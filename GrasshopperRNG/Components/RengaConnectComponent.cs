using System;
using System.Drawing;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Attributes;
using Grasshopper.Kernel.Parameters;
using GrasshopperRNG.Client;

namespace GrasshopperRNG.Components
{
    /// <summary>
    /// Component for connecting to Renga TCP server
    /// Main node that manages connection and data transmission
    /// </summary>
    public class RengaConnectComponent : GH_Component
    {
        private RengaGhClient client;
        private bool updateButtonPressed = false;

        public RengaConnectComponent()
            : base("RNG", "RNG",
                "Main node: Connect to Renga and manage data transmission",
                "RNG", "Main")
        {
        }

        public override void AppendAdditionalMenuItems(System.Windows.Forms.ToolStripDropDown menu)
        {
            base.AppendAdditionalMenuItems(menu);
            menu.Items.Add(new System.Windows.Forms.ToolStripSeparator());
            var updateItem = new System.Windows.Forms.ToolStripMenuItem("Update - Refresh Connection");
            updateItem.Click += (s, e) => OnUpdateButtonClick();
            menu.Items.Add(updateItem);
        }

        public override void CreateAttributes()
        {
            m_attributes = new RengaConnectComponentAttributes(this);
        }

        public void OnUpdateButtonClick()
        {
            updateButtonPressed = true;
            ExpireSolution(true);
        }

        protected override void RegisterInputParams(GH_InputParamManager pManager)
        {
            pManager.AddIntegerParameter("Port", "P", "TCP server port number (default: 50100)", GH_ParamAccess.item, 50100);
            pManager.AddBooleanParameter("Connect", "C", "Enable/disable connection", GH_ParamAccess.item, false);
        }

        protected override void RegisterOutputParams(GH_OutputParamManager pManager)
        {
            pManager.AddBooleanParameter("Connected", "C", "Connection status", GH_ParamAccess.item);
            pManager.AddTextParameter("Message", "M", "Status message", GH_ParamAccess.item);
            pManager.AddGenericParameter("Client", "Client", "Client object for other components", GH_ParamAccess.item);
        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            int port = 50100;
            bool connect = false;

            DA.GetData(0, ref port);
            DA.GetData(1, ref connect);

            // Reset update button flag after processing
            bool wasUpdatePressed = updateButtonPressed;
            updateButtonPressed = false;

            // Always ensure client exists
            if (client == null)
            {
                client = new RengaGhClient { Port = port };
            }
            else if (client.Port != port)
            {
                client.Disconnect();
                client = new RengaGhClient { Port = port };
            }

            // Handle connection/disconnection
            if (connect && !client.IsConnected)
            {
                if (client.Connect())
                {
                    DA.SetData(0, true);
                    DA.SetData(1, $"Connected to Renga on port {port}");
                    DA.SetData(2, new RengaGhClientGoo(client));
                }
                else
                {
                    DA.SetData(0, false);
                    DA.SetData(1, $"Failed to connect to Renga on port {port}. Make sure Renga plugin is running.");
                    DA.SetData(2, new RengaGhClientGoo(client)); // Still output client object
                }
            }
            else if (!connect && client.IsConnected)
            {
                client.Disconnect();
                DA.SetData(0, false);
                DA.SetData(1, "Disconnected from Renga");
                DA.SetData(2, new RengaGhClientGoo(client)); // Still output client object
            }
            else if (wasUpdatePressed && client.IsConnected)
            {
                // Update button pressed - refresh connection status
                DA.SetData(0, true);
                DA.SetData(1, $"Connected to Renga on port {port} (refreshed)");
                DA.SetData(2, new RengaGhClientGoo(client));
            }
            else
            {
                // Always output client, even if not connected (so Input component can see it)
                DA.SetData(0, client.IsConnected);
                DA.SetData(1, client.IsConnected ? "Connected" : "Not connected");
                DA.SetData(2, new RengaGhClientGoo(client)); // Always output client object
            }
        }

        protected override Bitmap Icon
        {
            get
            {
                // TODO: Add icon
                return null;
            }
        }

        public override Guid ComponentGuid => new Guid("7A8B9C0D-1E2F-3456-789A-BCDEF0123456");
    }
}

