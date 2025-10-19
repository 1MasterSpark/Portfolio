using System;
using SplashKitSDK;
using System.Diagnostics;

namespace tetris {
    public class Program {
        public static int _length = 30;
        public static int _width = 11;
        public static int _height = 20;

        public static void Main() {
            new Window("Tetris", 600, 660);
            Game game = Game.Instance();
            Stopwatch timer = new Stopwatch();
            timer.Start();
            TimeSpan lastUpdateTime = timer.Elapsed;
            SplashKit.LoadMusic("tetrisTheme", "music/Tetris.mp3");
            SplashKit.PlayMusic("tetrisTheme", 10);
            double interval = 0.5;
            double speedinterval = interval;

            do {
                SplashKit.ProcessEvents();
                SplashKit.ClearScreen();
                TimeSpan elapsedTime = timer.Elapsed - lastUpdateTime;
                interval = 1.0 / (game._score / 20.0 + 1) / 2;
                if (elapsedTime.TotalSeconds >= speedinterval) {
                    game.Run();
                    lastUpdateTime = timer.Elapsed;
                }

                if (SplashKit.KeyTyped(KeyCode.LeftKey)){
                    game.Move(-1,0);
                }
                if (SplashKit.KeyTyped(KeyCode.RightKey)){
                    game.Move(1,0);
                }
                if (SplashKit.KeyTyped(KeyCode.DownKey)){
                    game.Move(0,1);
                }
                if (SplashKit.KeyDown(KeyCode.DownKey)){
                    speedinterval = interval/5;
                } else {
                    speedinterval = interval;
                }
                if (SplashKit.KeyTyped(KeyCode.UpKey)){
                    game.Rotate();
                }
                if (SplashKit.KeyTyped(KeyCode.RightShiftKey)) {
                    game.HoldTetromino();
                }

                game.Draw();
                SplashKit.RefreshScreen();
            } while (!SplashKit.WindowCloseRequested("Tetris"));
        }
    }
}