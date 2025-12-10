using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using Grasshopper.GUI.Canvas;
using Grasshopper.Kernel.Attributes;

namespace GrasshopperRNG.Components
{
    /// <summary>
    /// Custom attributes for RengaConnectComponent with Update button
    /// </summary>
    public class RengaConnectComponentAttributes : GH_ComponentAttributes
    {
        public RengaConnectComponentAttributes(RengaConnectComponent owner) : base(owner)
        {
        }

        protected override void Layout()
        {
            base.Layout();

            // Extend bounds to include button at the bottom
            var extendedBounds = Bounds;
            extendedBounds.Height += 22; // Add space for button (20px + 2px margin)
            Bounds = extendedBounds;

            // Position button at the bottom of the component
            var buttonBounds = new RectangleF(
                Bounds.Left + 1,
                Bounds.Bottom - 21,
                Bounds.Width - 2,
                20
            );

            // Store button bounds for click detection
            ButtonBounds = buttonBounds;
        }

        private RectangleF ButtonBounds { get; set; }

        protected override void Render(GH_Canvas canvas, Graphics graphics, GH_CanvasChannel channel)
        {
            // Render base component first
            base.Render(canvas, graphics, channel);

            // Draw button in Objects channel (after base rendering)
            if (channel == GH_CanvasChannel.Objects)
            {
                graphics.SmoothingMode = SmoothingMode.AntiAlias;

                var buttonRect = ButtonBounds;
                var buttonRadius = 2.0f;

                using (var buttonPath = new GraphicsPath())
                {
                    buttonPath.AddArc(buttonRect.X, buttonRect.Y, buttonRadius * 2, buttonRadius * 2, 180, 90);
                    buttonPath.AddArc(buttonRect.Right - buttonRadius * 2, buttonRect.Y, buttonRadius * 2, buttonRadius * 2, 270, 90);
                    buttonPath.AddArc(buttonRect.Right - buttonRadius * 2, buttonRect.Bottom - buttonRadius * 2, buttonRadius * 2, buttonRadius * 2, 0, 90);
                    buttonPath.AddArc(buttonRect.X, buttonRect.Bottom - buttonRadius * 2, buttonRadius * 2, buttonRadius * 2, 90, 90);
                    buttonPath.CloseFigure();

                    // Button background - Standard Grasshopper button gradient
                    using (var brush = new LinearGradientBrush(
                        new PointF(buttonRect.Left, buttonRect.Top),
                        new PointF(buttonRect.Left, buttonRect.Bottom),
                        Color.FromArgb(255, 255, 255, 255),      // White top
                        Color.FromArgb(255, 240, 240, 240)))    // Light gray bottom
                    {
                        var blend = new ColorBlend(3);
                        blend.Colors = new Color[] {
                            Color.FromArgb(255, 255, 255, 255),      // White 0%
                            Color.FromArgb(255, 248, 248, 248),      // Very light gray 50%
                            Color.FromArgb(255, 240, 240, 240)       // Light gray 100%
                        };
                        blend.Positions = new float[] { 0f, 0.5f, 1f };
                        brush.InterpolationColors = blend;

                        graphics.FillPath(brush, buttonPath);
                    }

                    // Button border
                    using (var pen = new Pen(Color.FromArgb(128, 0, 0, 0), 1))
                    {
                        graphics.DrawPath(pen, buttonPath);
                    }

                    // Inner highlight
                    using (var highlightPen = new Pen(Color.FromArgb(128, 255, 255, 255), 1))
                    {
                        var highlightRect = buttonRect;
                        highlightRect.Height = 1;
                        graphics.DrawLine(highlightPen, highlightRect.Left + buttonRadius, highlightRect.Top,
                            highlightRect.Right - buttonRadius, highlightRect.Top);
                    }

                    // Button text - Standard Grasshopper text color
                    using (var font = new Font("Arial", 8, FontStyle.Bold))
                    using (var brush = new SolidBrush(Color.FromArgb(255, 50, 50, 50))) // Dark gray text
                    {
                        var textRect = buttonRect;
                        var format = new StringFormat
                        {
                            Alignment = StringAlignment.Center,
                            LineAlignment = StringAlignment.Center
                        };
                        graphics.DrawString("Update", font, brush, textRect, format);
                    }
                }
            }
        }

        public override bool IsPickRegion(PointF point)
        {
            // Convert to local coordinates
            var localPoint = new PointF(point.X - Bounds.X, point.Y - Bounds.Y);
            
            // Check if point is within button bounds
            if (ButtonBounds.Contains(localPoint))
            {
                return true;
            }
            return base.IsPickRegion(point);
        }


    }
}

