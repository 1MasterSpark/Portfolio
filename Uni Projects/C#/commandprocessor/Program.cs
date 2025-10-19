using System;
using SplashKitSDK;

namespace commandprocessor {
    public class Program {
        public static void Main(string[] args) {
            Location dungeon = new Location(new string[] {"dungeon" }, "a dimly lit dungeon", "This place stinks! You don't remember how you got here");
            Location catacombs = new Location(new string[] {"catacombs", "tunnel"}, "gloomy, rat-infested catacombs", "The walls are lined with countless skulls");
            Location cathedral = new Location(new string[] {"cathedral", "church"}, "your hometown's gothic-style cathedral", "By far your hometown's most prominent building. This place is nostalgic for you");
            Console.WriteLine("Welcome to Swin Adventure!\n");

            Console.Write("Enter player name: ");
            string desc = Console.ReadLine();
            Console.Write("Enter player description: ");
            string longdesc = Console.ReadLine();
            Player player = new Player(desc, dungeon, longdesc);

            Bag pouch = new Bag(new string[] {"pouch" }, "a leather pouch", "A leather pouch with a nice design on it");
            Item gem = new Item(new string[] { "gem" }, "a shiny red gem", "This looks valuable, but should be appraised");
            Item sword = new Item(new string[] { "sword", "bronze sword" }, "a rusty bronze sword", "This sword has seen better days");
            Item shovel = new Item(new string[] { "shovel", "spade" }, "a fine shovel", "Doesn't look like anyone will miss this");
            Item candle = new Item(new string[] { "candle"}, "a lit wax candle", "The flame has dug a hole into this thick candle");
            Path brokentile = new Path(new string[] { "broken tile", "tile" }, "down", "a loose-looking tile", "There's some sort of tunnel there","There's light coming from below it", "You move the tile", "You squeeze into the gap where the tile was", catacombs);
            Path belowhatch = new Path(new string[] { "hatch" }, "up", "a hatch in the roof", "Someone dug out niches in the wall to access this", "You climb up through the hatch", cathedral);
            Path abovehatch = new Path(new string[] { "hatch" }, "down", "a hatch in the floor", "You never knew there were catacombs under the church", "You climb down through the hatch", catacombs);
            player.Inventory.Put(sword);
            player.Inventory.Put(shovel);
            dungeon.Inventory.Put(pouch);
            dungeon.Inventory.Put(brokentile);
            pouch.Inventory.Put(gem);
            catacombs.Inventory.Put(candle);
            catacombs.Inventory.Put(belowhatch);
            cathedral.Inventory.Put(abovehatch);
            Dictionary<string, Command> commands = new Dictionary<string, Command> {
                { "look", new Look() },
                { "move", new Move() }
            };

            string command = "";
            while (command != "quit") {
                Console.Write("> ");
                command = Console.ReadLine();
                string[] text = command.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);

                if (text.Length > 0) {
                    string commandKey = text[0].ToLower();

                    if (commands.ContainsKey(commandKey)) {
                        Command cmd = commands[commandKey];
                        cmd.Execute(player, text);
                    } else {
                        Console.WriteLine("Unknown command.\n");
                    }
                }
            }
        }
    }
}
