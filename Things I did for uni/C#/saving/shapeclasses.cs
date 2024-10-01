using System;
using SplashKitSDK;
using System.IO;

namespace saving{
    public abstract class Shape {
        protected Color _color;
        protected float _x;
        protected float _y;

        public Shape(float x = 0, float y = 0){
            //_color = SplashKit.RandomRGBColor(255);
            _color = Color.Yellow;
            _x = x;
            _y = y;
        }

        public abstract void Draw();
        public abstract void DrawOutline();
        public abstract bool IsAt(Point2D point);

        public virtual void SaveTo(StreamWriter writer) {
            writer.WriteColor(_color);
            writer.WriteLine(_x);
            writer.WriteLine(_y);
        }

        public virtual void LoadFrom(StreamReader reader) {
            Color = reader.ReadColor();
            X = reader.ReadInteger();
            Y = reader.ReadInteger();
        }

        public bool IsSelected(Drawing drawing){
            if (drawing.SelectedShapes.Contains(this)){
                return true;
            } else {
                return false;
            }
        }

        public Color Color{
            get{
                return _color;
            }
            set{
                _color = value;
            }
        }

        public float X{
            get{
                return _x;
            }
            set{
                _x = value;
            }
        }

        public float Y{
            get{
                return _y;
            }
            set{
                _y = value;
            }
        }
    }

    public class Drawing {
        private readonly List<Shape> _shapes;
        private readonly List<Shape> _selectedshapes;
        private Color _background;

        public Drawing(Color background){
            _shapes = new List<Shape>();
            _selectedshapes = new List<Shape>();
            _background = background;
        }

        public Drawing(): this (Color.White){
        }

        public Color Background{
            get{
                return _background;
            }
            set{
                _background = value;
            }
        }

        public int ShapeCount{
            get {
                return _shapes.Count;
            }
        }

        public List<Shape> SelectedShapes{
            get {
                return _selectedshapes;
            }
        }

        public void AddShape(Shape shape){
            _shapes.Add(shape); 
        }

        public void SelectShapesAt(Point2D pt){
            foreach (Shape s in _shapes){
                if (s.IsAt(pt)){
                    _selectedshapes.Add(s); 
                }
            }
        }

        public void Draw(){
            SplashKit.FillRectangle(_background, 0, 0, SplashKit.ScreenWidth(), SplashKit.ScreenHeight());
            for (int i = 0; i < _shapes.Count; i++){
                if (_shapes[i].IsSelected(this)){
                    _shapes[i].DrawOutline();
                }
                _shapes[i].Draw();
            }
        }

        public void Delete() {
            foreach (Shape s in _selectedshapes) {
                _shapes.Remove(s);
            }
            _selectedshapes.Clear();
        }

        public void Save(string filename) {
            StreamWriter writer = new StreamWriter(filename);
            try {
                writer.WriteColor(_background);
                writer.WriteLine(_shapes.Count);
                foreach (Shape s in _shapes) {
                    s.SaveTo(writer);
                }
            } finally {
            writer.Close();
            }
        }

        public void Load(string filename) {
            StreamReader reader = new StreamReader(filename);
            try {
                Background = reader.ReadColor();
                int count = reader.ReadInteger();
                _shapes.Clear();

                for (int i = 0; i < count; i++) {
                    string kind = reader.ReadLine();
                    Shape s;
                    switch (kind) {
                        case "Rectangle":
                            s = new Rectangle(100, 100);
                            break;
                        case "Circle":
                            s = new Circle(100, 100);
                            break;
                        case "Line":
                            s = new Line(100, 100);
                            break;
                        default:
                            throw new InvalidDataException("Uknown shape kind: " + kind);
                    }
                    s.LoadFrom(reader);
                    AddShape(s);
                }
            } finally {
            reader.Close();
            }
        }
    }

    public class Rectangle : Shape{
        private int _width;
        private int _height;

        public Rectangle(float x, float y, int width = 100, int height = 100) : base(x, y) {
            _width = width;
            _height = height;
            Color = Color.Green;
        }

        public override void Draw(){
            SplashKit.FillRectangle(Color, X, Y, _width, _height);  
        }

        public override void DrawOutline(){
            SplashKit.FillRectangle(Color.Black, X - 2, Y - 2, _width + 4, _height + 4);  
        }

        public override bool IsAt(Point2D point){
            if (point.X >= X && point.X <= X + _width && point.Y >= Y && point.Y <= Y + _height){
                return true;
            } else {
                return false;
            }
        }

        public override void SaveTo(StreamWriter writer) {
            writer.WriteLine("Rectangle");
            base.SaveTo(writer);
            writer.WriteLine(_width);
            writer.WriteLine(_height);
        }

        public override void LoadFrom(StreamReader reader) {
            base.LoadFrom(reader);
            Width = reader.ReadInteger();
            Height = reader.ReadInteger();
        }

        public int Width {
            get {
                return _width;
            }
            set {
                _width = value;
            }
        }

        public int Height {
            get {
                return _height;
            }
            set {
                _height = value;
            }
        }
    }

    public class Circle : Shape {
        private int _radius;

        public Circle(float x, float y, int radius = 50) : base(x, y) {
            _radius = radius;
            Color = Color.Blue;
        }

        public override void Draw(){
            SplashKit.FillCircle(Color, X, Y, _radius);
        }

        public override void DrawOutline(){
            SplashKit.FillCircle(Color.Black, X, Y, _radius + 2);  
        }

        public override bool IsAt(Point2D point){
            float dx = (float)point.X - X;
            float dy = (float)point.Y - Y;
            float distance2 = dx * dx + dy * dy;
            return distance2 <= _radius * _radius;
        }

        public override void SaveTo(StreamWriter writer) {
            writer.WriteLine("Circle");
            base.SaveTo(writer);
            writer.WriteLine(_radius);
        }

        public override void LoadFrom(StreamReader reader) {
            base.LoadFrom(reader);
            Radius = reader.ReadInteger();
        }

        public int Radius {
            get {
                return _radius;
            }
            set {
                _radius = value;
            }
        }
    }

    public class Line : Shape {
        private float _endX;
        private float _endY;

        public Line(float x, float y, float endX = 100, float endY = 100) : base(x, y) {
            _endX = endX;
            _endY = endY;
            Color = Color.Red;
        }

        public override void Draw() {
            SplashKit.DrawLine(Color, X, Y, _endX, _endY);
        }

        public override void DrawOutline() {
            SplashKit.FillCircle(Color.Black, X, Y, 2);
            SplashKit.FillCircle(Color.Black, _endX, _endY, 2);
        }

        public override bool IsAt(Point2D point) {
            float dx = _endX - X;
            float dy = _endY - Y;
            float numerator = dx * (Y - (float)point.Y) - dy * (X - (float)point.X);
            float d2 = (numerator * numerator)/(dx * dx + dy * dy);
            return d2 <= 100;
        }

        public override void SaveTo(StreamWriter writer) {
            writer.WriteLine("Line");
            base.SaveTo(writer);
            writer.WriteLine(_endX);
            writer.WriteLine(_endY);
        }

        public override void LoadFrom(StreamReader reader) {
            base.LoadFrom(reader);
            EndX = reader.ReadInteger();
            EndY = reader.ReadInteger();
        }

        public float EndX {
            get {
                return _endX;
            }
            set {
                _endX = value;
            }
        }

        public float EndY {
            get {
                return _endY;
            }
            set {
                _endY = value;
            }
        }
    }

    public static class ExtensionMethods {
        public static int ReadInteger(this StreamReader reader) {
            return Convert.ToInt32(reader.ReadLine ());
        }
        public static float ReadSingle(this StreamReader reader) {
            return Convert.ToSingle(reader.ReadLine ());
        }
        public static Color ReadColor(this StreamReader reader) {
            return Color.RGBColor(reader.ReadSingle(), reader.ReadSingle(), reader.ReadSingle());
        }
        public static void WriteColor(this StreamWriter writer, Color clr) {
        writer.WriteLine("{0}\n{1}\n{2}", clr.R, clr.G, clr.B);
        }
    }
}