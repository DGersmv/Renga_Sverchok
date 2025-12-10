using Grasshopper.Kernel;
using System;
using System.Drawing;
using System.Collections.Generic;
using GrasshopperRNG.Components;

namespace GrasshopperRNG.Properties
{
    /// <summary>
    /// Assembly info for Grasshopper plugin registration
    /// This class is automatically discovered by Grasshopper to register the plugin
    /// </summary>
    public class GrasshopperInfo : GH_AssemblyInfo
    {
        public override string Name => "GrasshopperRNG";
        public override Bitmap Icon => null; // Icon will be set by category
        public override string Description => "GrasshopperRNG Integration - Create columns in Renga from Grasshopper points";
        public override Guid Id => new Guid("9C0D1E2F-3456-789A-BCDE-F01234567890");
        public override string AuthorName => "Renga Software LLC";
        public override string AuthorContact => "";
        public override string Version => "1.0.0.0";
    }
}

