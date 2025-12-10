using System;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace GrasshopperRNG.Client
{
    /// <summary>
    /// TCP client for communicating with Renga plugin
    /// Updated: Improved response reading and reconnection logic
    /// </summary>
    public class RengaGhClient
    {
        private TcpClient tcpClient;
        private NetworkStream stream;
        
        public string Host { get; set; } = "127.0.0.1";
        public int Port { get; set; } = 50100;
        public TimeSpan Timeout { get; set; } = TimeSpan.FromSeconds(10);
        public bool IsConnected => tcpClient != null && tcpClient.Connected;

        /// <summary>
        /// Connect to Renga TCP server
        /// </summary>
        public bool Connect()
        {
            try
            {
                tcpClient = new TcpClient();
                var connectTask = tcpClient.ConnectAsync(Host, Port);
                if (connectTask.Wait(Timeout))
                {
                    if (tcpClient.Connected)
                    {
                        stream = tcpClient.GetStream();
                        return true;
                    }
                }
                return false;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Disconnect from server
        /// </summary>
        public void Disconnect()
        {
            stream?.Close();
            tcpClient?.Close();
            stream = null;
            tcpClient = null;
        }

        /// <summary>
        /// Send JSON data to server and get response
        /// </summary>
        public string Send(string jsonData)
        {
            // Check connection status
            if (tcpClient == null || !tcpClient.Connected || stream == null)
            {
                System.Diagnostics.Debug.WriteLine("Send failed: Not connected or stream is null. Attempting to reconnect...");
                // Try to reconnect
                if (!Connect())
                {
                    System.Diagnostics.Debug.WriteLine("Reconnection failed");
                    return null;
                }
            }

            try
            {
                stream.ReadTimeout = 10000; // 10 second timeout
                
                // Send data
                var data = Encoding.UTF8.GetBytes(jsonData);
                System.Diagnostics.Debug.WriteLine($"Sending {data.Length} bytes to server");
                stream.Write(data, 0, data.Length);
                stream.Flush();

                // Wait for response - server needs time to process
                System.Threading.Thread.Sleep(200);

                // Read response - try multiple times
                var buffer = new List<byte>();
                var readBuffer = new byte[8192];
                int totalBytesRead = 0;
                int attempts = 0;
                const int maxAttempts = 50; // 5 seconds total (50 * 100ms)
                
                while (attempts < maxAttempts)
                {
                    if (stream.DataAvailable)
                    {
                        int bytesRead = stream.Read(readBuffer, 0, readBuffer.Length);
                        if (bytesRead > 0)
                        {
                            for (int i = 0; i < bytesRead; i++)
                            {
                                buffer.Add(readBuffer[i]);
                            }
                            totalBytesRead += bytesRead;
                            
                            // Check if we have complete JSON (look for closing brace)
                            var currentString = Encoding.UTF8.GetString(buffer.ToArray());
                            if (currentString.TrimEnd().EndsWith("}") || currentString.TrimEnd().EndsWith("]"))
                            {
                                // Might be complete, wait a bit more to be sure
                                System.Threading.Thread.Sleep(100);
                                if (!stream.DataAvailable)
                                {
                                    break; // Complete message received
                                }
                            }
                        }
                    }
                    else
                    {
                        // No data yet, wait a bit
                        System.Threading.Thread.Sleep(100);
                    }
                    attempts++;
                }
                
                if (buffer.Count > 0)
                {
                    var response = Encoding.UTF8.GetString(buffer.ToArray());
                    System.Diagnostics.Debug.WriteLine($"Received {buffer.Count} bytes from server");
                    return response;
                }
                else
                {
                    System.Diagnostics.Debug.WriteLine("No response received from server");
                    return null;
                }
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error sending data: {ex.Message}");
                System.Diagnostics.Debug.WriteLine($"Stack trace: {ex.StackTrace}");
                return null;
            }
        }

        public void Dispose()
        {
            Disconnect();
        }
    }
}

