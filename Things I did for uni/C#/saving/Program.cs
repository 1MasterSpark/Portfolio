using System;
using SplashKitSDK;

namespace saving {
    public class Program {
        private enum ShapeKind{
            Rectangle, Circle, Line
        }

        private static Point2D _lineStart;
        private static Point2D _lineEnd;
        private static bool drawingline = false;

        public static void Main() {
            new Window("Drawings", 800, 600);
            Drawing myDrawing = new Drawing();
            ShapeKind kindToAdd = ShapeKind.Circle;

            do {
                SplashKit.ProcessEvents();
                SplashKit.ClearScreen();
                Point2D mousePoint = new Point2D();

                if (SplashKit.MouseClicked(MouseButton.LeftButton)){
                    mousePoint.X = SplashKit.MouseX();
                    mousePoint.Y = SplashKit.MouseY();
                    Shape? newShape = null;

                    if (kindToAdd == ShapeKind.Rectangle){
                        Rectangle newRect = new Rectangle((float)mousePoint.X - 50, (float)mousePoint.Y - 50);
                        newShape = newRect;

                    } else if (kindToAdd == ShapeKind.Circle){
                        Circle newCirc = new Circle((float)mousePoint.X, (float)mousePoint.Y);
                        newShape = newCirc;

                    } else if (kindToAdd == ShapeKind.Line){
                        if (!drawingline) {
                            _lineStart = mousePoint;
                            drawingline = true;

                        } else {
                            _lineEnd = mousePoint;
                            Line newLine = new Line((float)_lineStart.X, (float)_lineStart.Y, (float)_lineEnd.X, (float)_lineEnd.Y);
                            newShape = newLine;
                            drawingline = false;
                        }
                    }
                    if (newShape != null) {
                        myDrawing.AddShape(newShape);
                    }
                }

                if (SplashKit.MouseClicked(MouseButton.RightButton)){
                    mousePoint.X = SplashKit.MouseX();
                    mousePoint.Y = SplashKit.MouseY();
                    myDrawing.SelectShapesAt(mousePoint);
                    foreach (Shape s in myDrawing.SelectedShapes){
                        s.DrawOutline();
                    }
                }

                if (SplashKit.KeyDown(KeyCode.SpaceKey)) {
                    myDrawing.Background = SplashKit.RandomRGBColor(255);
                }

                if (SplashKit.KeyTyped(KeyCode.DeleteKey)) {
                    myDrawing.Delete();
                }

                if (SplashKit.KeyTyped(KeyCode.RKey)) {
                    kindToAdd = ShapeKind.Rectangle;
                }
                
                if (SplashKit.KeyTyped(KeyCode.CKey)) {
                    kindToAdd = ShapeKind.Circle;
                }

                if (SplashKit.KeyTyped(KeyCode.LKey)) {
                    kindToAdd = ShapeKind.Line;
                    drawingline = false;
                }

                if (SplashKit.KeyTyped(KeyCode.SKey)) {
                    string filePath = "C:\\Users\\mamdo\\OneDrive\\Desktop\\mark\\C#\\saving\\TestDrawing.txt";
                    myDrawing.Save(filePath);
                }

                if (SplashKit.KeyTyped(KeyCode.OKey)) {
                    try {
                        string filePath = "C:\\Users\\mamdo\\OneDrive\\Desktop\\mark\\C#\\saving\\TestDrawing.txt";
                        myDrawing.Load(filePath);
                    } catch (Exception e) {
                        Console.Error.WriteLine("Error loading file: {0}", e.Message);
                    }
                }

                myDrawing.Draw();
                SplashKit.RefreshScreen();
            } while (!SplashKit.WindowCloseRequested("Drawings"));
        }
    }
}
