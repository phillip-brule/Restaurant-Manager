using System;
using System.Collections.Generic;
using System.Text;

namespace RestaurantManagerData.Models
{
    public abstract class User
    {
        public int id { get; set; }
        public String firstName { get; set; }
        public String lastName { get; set; }
        public String email { get; set; }
    }
}
