using Microsoft.EntityFrameworkCore;
using RestaurantManagerData.Models;

namespace RestaurantManagerData
{
    public class RestaurantManagerContext : DbContext
    {
        public RestaurantManagerContext(DbContextOptions options) : base(options) { }

        public DbSet<User> Users { get; set; }
        
        public DbSet<Manager> Managers { get; set; }



        public DbSet<Restaurant> Restaurants { get; set; }


    }
}
