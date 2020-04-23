using RestaurantManagerData.Models;
using Microsoft.EntityFrameworkCore;

namespace RestaurantManagerData
{
    class RestaurantManagerDbContext : DbContext
    {
       public RestaurantManagerDbContext()
        {

        }

        public RestaurantManagerDbContext(DbContextOptions options) : base(options)
        {

        }

        public virtual DbSet<User> Users { get; set; }
        public virtual DbSet<Restaurant> Restaurants { get; set; }
        public virtual DbSet<Manager> Managers { get; set; }
    }
}
