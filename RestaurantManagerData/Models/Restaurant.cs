using System;
using System.Collections.Generic;
using System.Text;

namespace RestaurantManagerData.Models
{
    public class Restaurant
    {
        public String name { get; set; }
        public List<User> userList { get; set; } 
    }
}
