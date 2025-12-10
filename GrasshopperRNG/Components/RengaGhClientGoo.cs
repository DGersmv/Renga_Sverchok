using System;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Types;
using GrasshopperRNG.Client;

namespace GrasshopperRNG.Components
{
    /// <summary>
    /// GH_Goo wrapper for RengaGhClient to pass between components
    /// </summary>
    public class RengaGhClientGoo : GH_Goo<RengaGhClient>
    {
        public RengaGhClientGoo()
        {
        }

        public RengaGhClientGoo(RengaGhClient client)
        {
            Value = client;
        }

        public override bool IsValid => Value != null;

        public override string TypeName => "RengaGhClient";

        public override string TypeDescription => "Renga TCP Client for Grasshopper";

        public override IGH_Goo Duplicate()
        {
            return new RengaGhClientGoo(Value);
        }

        public override string ToString()
        {
            if (Value == null)
                return "Null RengaGhClient";
            
            return Value.IsConnected 
                ? $"RengaGhClient (Connected on port {Value.Port})" 
                : $"RengaGhClient (Not connected)";
        }

        public override bool CastFrom(object source)
        {
            if (source is RengaGhClient client)
            {
                Value = client;
                return true;
            }
            return false;
        }

        public bool CastTo<T>(out T target)
        {
            if (typeof(T).IsAssignableFrom(typeof(RengaGhClient)))
            {
                target = (T)(object)Value;
                return true;
            }
            target = default(T);
            return false;
        }
    }
}

