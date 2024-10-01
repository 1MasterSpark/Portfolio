using System;
using System.Collections.Generic;

namespace commandprocessor {
    public abstract class Command {
        protected readonly List<string> _identifiers;
        protected string _name;

        public Command(string[] idents, string name){
            _identifiers = new List<string>(idents);
            _name = name;
        }

        public bool AreYou(string iden){
            bool areyou = false; 
            for (int i = 0; i < _identifiers.Count; i++){
                if (string.Equals(_identifiers[i], iden, StringComparison.OrdinalIgnoreCase)){
                areyou = true;
                break;
                }
            }
            return areyou;
        }

        public abstract void Execute(Player me, string[] text);

        public void AddIdentifier(string iden){
            _identifiers.Add(iden);  
        }
    }

    public class Look : Command {
        public Look() : base(new string[] { "look" }, "Look") {
        }
        
        public override void Execute(Player p, string[] text) {
            if (text.Length != 3 && text.Length != 5) {
                Console.WriteLine("I don't know how to look like that\n");
                return;
            }

            if (!this.AreYou(text[0])) {
                Console.WriteLine("Error in look input: command doesn't start with 'look'\n");
                return;
            }

            if (!text[1].Equals("at", StringComparison.OrdinalIgnoreCase) && !text[1].Equals("for", StringComparison.OrdinalIgnoreCase)) {
                Console.WriteLine("What do you want to look at?\n");
                return;
            }

            if (text.Length == 5 && p.Locate(text[4]) != p) {
                if (!text[3].Equals("in", StringComparison.OrdinalIgnoreCase)) {
                    Console.WriteLine("What do you want to look in?\n");
                    return;
                }

                GameObject containersearch = p.Locate(text[4]);
                if (containersearch == null){
                    Console.WriteLine($"I can't find the {text[4]}\n");
                    return;
                } else if (containersearch is Bag){
                    Bag container = containersearch as Bag;
                    GameObject thing = container.Locate(text[2]);
                    if (thing == null){
                        string containername = containersearch.FirstId;
                        Console.WriteLine($"I can't find the {text[2]} in the {containername}\n");
                    } else {
                        Console.WriteLine(thing.LongDesc);
                    }
                } else if (containersearch is Location){
                    Location container = containersearch as Location;
                    GameObject thing = container.Locate(text[2]);
                    if (thing == null){
                        string containername = containersearch.FirstId;
                        Console.WriteLine($"I can't find the {text[2]} in the {containername}\n");
                    } else {
                        Console.WriteLine(thing.LongDesc);
                    }
                } else {
                    Console.WriteLine($"I can't look in the {text[4]}\n");
                    return;
                }
            } else {
                GameObject thing = p.Locate(text[2]);
                if (thing == null){
                    Console.WriteLine($"I can't find the {text[2]} here or in your inventory\n");
                } else {
                    Console.WriteLine(thing.LongDesc);
                }
            }
        }
    }

    public class Move : Command {
        public Move() : base(new string[] { "move", "go" }, "Move") {
        }
        
        string destString;
        public override void Execute(Player p, string[] text) {
            if (text.Length == 3) {
                destString = text[2];
            } else if (text.Length == 2){
                destString = text[1];
            } else {
                Console.WriteLine("I don't know how to look like that\n");
                return;
            }

            if (!this.AreYou(text[0])) {
                Console.WriteLine("Error in move input: command doesn't start with 'move' or 'go'\n");
                return;
            }

            GameObject destObject = p.Location.Locate(destString);
            if (destObject == null){
                Console.WriteLine($"I can't find the {destString}\n");
            } else if (destObject is Path){
                Path destPath = destObject as Path;
                destPath.Use(p);
            } else {
                Console.WriteLine($"You can't go through the {destString}\n");
            }
        }
    }
    
    public abstract class GameObject {
        protected readonly List<string> _identifiers;
        protected string _desc;

        public GameObject(string[] idents, string desc){
            _identifiers = new List<string>(idents);
            _desc = desc;
        }

        public string FirstId {
            get{
                return _identifiers[0];
            }
        }

        public string ShortDesc {
            get{
                return $"{_desc}\n";
            }
        }

        public virtual string LongDesc {
            get{
                return null;
            }
        }

        public bool AreYou(string iden){
            bool areyou = false; 
            for (int i = 0; i < _identifiers.Count; i++){
                if (string.Equals(_identifiers[i], iden, StringComparison.OrdinalIgnoreCase)){
                areyou = true;
                break;
                }
            }
            return areyou;
        }

        public void AddIdentifier(string iden){
            _identifiers.Add(iden);  
        }
    }

    public class Item : GameObject {
        protected string _longDesc;

        public Item(string[] idents, string desc, string longDesc = null) : base(idents, desc) {
            _longDesc = longDesc;
        }

        public override string LongDesc {
            get {
                string result = this.ShortDesc;
                if (_longDesc != null){
                    result += $"{_longDesc}\n";
                }
                return result;
            }
        }
    }   

    public class Inventory{
        private List<GameObject> _items;

        public Inventory(){
            _items = new List<GameObject>();
        }

        public void Put(GameObject item){
            _items.Add(item);
        }

        public Item Take(string id){
            GameObject item = Fetch(id);
            if (item != null) {
                if (item is Item) {
                    _items.Remove(item);
                    return (Item)item;
                } else {
                    Console.WriteLine("You can't take that.");
                    return null;
                }
            }
            return null;
        }

        public GameObject Fetch(string id){
            foreach (GameObject item in _items) {
                if (item.AreYou(id)) {
                    return item;
                }
            }
            return null;
        }

        public string ItemList{
            get{
                string result = "";
                foreach (GameObject item in _items) {
                    result += $"    {item.ShortDesc}";
                }
                return result;
            }
        }
    }

    public class Player : GameObject{
        private Inventory _inventory;
        protected Location _location;
        protected string _longDesc;

        public Player(string desc, Location location, string longDesc = null) : base(new string[]{"me", "inventory"}, desc) {
            _inventory = new Inventory();
            _location = location;
            _longDesc = longDesc;
        }

        public override string LongDesc {
            get{
                string result = this.ShortDesc;
                if (_longDesc != null){
                    result += $"{_longDesc}\n";
                }
                result += "You are in " + _location.ShortDesc;
                result += "You are carrying\n";
                result += _inventory.ItemList;
                return result;
            }
        }

        public GameObject Locate(string id){
            if (this.AreYou(id)){
                return this;
            } else {
                GameObject item = _inventory.Fetch(id);
                if (item != null){
                    return item;
                } else {
                    item = _location.Locate(id);
                    return item;
                }
            }
        }

        public Inventory Inventory {
            get{
                return _inventory;
            }
        }

        public Location Location{
            get{
                return _location;
            }
            set{
                _location = value;
            }
        }
    }

    public class Bag : Item {
        private Inventory _inventory;

        public Bag(string[] idents, string desc, string longDesc = null) : base(idents, desc) {
            _inventory = new Inventory();
            _longDesc = longDesc;
        }

        public GameObject Locate(string id) {
            if (this.AreYou(id)) {
                return this;
            } else {
                GameObject item = _inventory.Fetch(id);
                return item;
            }
        }

        public Inventory Inventory {
            get {
                return _inventory;
            }
        }

        public override string LongDesc {
            get{
                string result = this.ShortDesc;
                if (_longDesc != null){
                    result += $"{_longDesc}\n";
                }
                result += "In the " + _identifiers[0] + " you can see\n";
                result += _inventory.ItemList;
                return result;
            }
        }
    }

    public class Location : Item {
        private Inventory _inventory;
        public Location(string[] idents, string desc, string longDesc = null) : base(idents, desc) {
            _inventory = new Inventory();
            _longDesc = longDesc;
        }

        public GameObject Locate(string id) {
            if (this.AreYou(id)) {
                return this;
            } else {
                GameObject item = _inventory.Fetch(id);
                if (item != null) {
                    return item;
                } else {
                    return null;
                }
            }
        }

        public Inventory Inventory {
            get {
                return _inventory;
            }
        }

        public override string LongDesc {
            get {
                string result = this.ShortDesc;
                if (_longDesc != null){
                    result += $"{_longDesc}\n";
                }
                result += "You can see\n";
                result += _inventory.ItemList;
                return result;
            }
        }
    }

    public class Path : GameObject {
        protected bool _islocked;
        protected string _lockedDesc;
        protected string _unlockedDesc;
        protected string _unlockMessage;
        protected string _useMessage;
        protected string _direction;
        protected Location _exit;

        public Path(string[] idents, string direction, string desc, string unlockedDesc, string lockedDesc, string unlockMessage, string useMessage, Location exit, bool islocked = true) : base(idents, desc) {
            _unlockedDesc = unlockedDesc;
            _lockedDesc = lockedDesc;
            _islocked = islocked;
            _unlockMessage = unlockMessage;
            _exit = exit;
            _useMessage = useMessage;
            _direction = direction;
            this.AddIdentifier(direction);
        }

        public Path(string[] idents, string direction, string desc, string unlockedDesc, string useMessage, Location exit) : base(idents, desc) {
            _unlockedDesc = unlockedDesc;
            _lockedDesc = null;
            _unlockMessage = null;
            _islocked = false;
            _exit = exit;
            _useMessage = useMessage;
            _direction = direction;
            this.AddIdentifier(direction);
        }

        public override string LongDesc {
            get {
                string result = this.ShortDesc;
                if (_islocked){
                    result += $"{_lockedDesc}\n";
                } else {
                    result += $"{_unlockedDesc}\n";
                }
                return result;
            }
        }

        public void Unlock() {
            if (_islocked) {
                _islocked = false;
                Console.WriteLine(_unlockMessage + "\n");
            } else {
                Console.WriteLine("It's already unlocked\n");
            } 
        }

        public void Use(Player player) {
            if (_islocked) {
                Console.WriteLine("It's locked\n");
            } else {
                player.Location = _exit;
                Console.WriteLine(_useMessage + "\n");
            }
        }
    }  
}