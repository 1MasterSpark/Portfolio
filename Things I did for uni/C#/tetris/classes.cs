using System;
using SplashKitSDK;
using System.IO;

namespace tetris{
    public class Block {
        public Color _color;
        protected int _x;
        protected int _y;
        protected volatile bool _isFull;

        public Block(int x, int y, Color color){
            _color = color;
            _x = x;
            _y = y;
            _isFull = false;
        }

        public void Draw() {
            SplashKit.FillRectangle(_color, _x * Program._length + Program._length, _y * Program._length + Program._length, Program._length, Program._length);
        }

        public void Colour(Color color) {
            _isFull = true;
            _color = color;
        }

        public void Clear(){
            _isFull = false;
            _color = Color.White;
        }

        public bool IsFull{
            get{return _isFull;}
            set{_isFull = value;}
        }

        public int X{
            get{return _x;}
            set{_x = value;}
        }

        public int Y{
            get{return _y;}
            set{_y = value;}
        }
    }

    public abstract class Tetromino {
        public Color _color;
        public int _x;
        public int _y;
        public Block[] _blocks;

        public Tetromino(int x, int y){
            _color = SplashKit.RandomRGBColor(255);
            _x = x;
            _y = y;
            _blocks = new Block[4];
        }

        public void Draw(){
            foreach (Block b in _blocks) {
                b.Draw();
            }
        }

        public void Move(int dx, int dy){
            _x = _x + dx;
            _y = _y + dy;
            foreach (Block b in _blocks){
                b.X = b.X + dx;
                b.Y = b.Y + dy;
            }
        }

        public void Set(int x, int y){
            int dx = x - _x;
            int dy = y - _y;
            _x = _x + dx;
            _y = _y + dy;
            foreach (Block b in _blocks){
                b.X = b.X + dx;
                b.Y = b.Y + dy;
            }
        }

        public Block[] rotatedBlocks(){
            Block[] rotatedBlocks = new Block[4];
            for (int i = 0; i < 4; i++) {
                int newX = _x + (_blocks[i].Y - _y);
                int newY = _y - (_blocks[i].X - _x);
                rotatedBlocks[i] = new Block(newX, newY, _color);
            }
            return rotatedBlocks;
        }
    }

    public class Game {
        private static Game _instance;
        public Block[][] _grid;
        public Tetromino _tetromino;
        private Tetromino _nextTetromino;
        private Tetromino _savedTetromino;
        public int _score;
        public int _highscore;
        private bool _gameOver;

        private Game(){
            _gameOver = false;
            _score = 0;
            _highscore = GetHighscore();
            _grid = new Block[Program._width][];
            for (int i = 0; i < Program._width; i++){
                _grid[i] = new Block[Program._height];
                for (int j = 0; j < Program._height; j++){
                    _grid[i][j] = new Block(i, j, Color.White);
                }
            }
            _nextTetromino = RandomTetromino(Program._width + 2,1);
            AddTetromino();
        }

        public void Draw(){
            SplashKit.FillRectangle(Color.LightGreen, 0, 0, SplashKit.ScreenWidth(), SplashKit.ScreenHeight());
            SplashKit.FillRectangle(Color.White, Program._length, Program._length, Program._width * Program._length, Program._height * Program._length);
            for (int i = 0; i < Program._width; i++){
                for (int j = 0; j < Program._height; j++){
                    _grid[i][j].Draw();
                }
            }

            SplashKit.FillRectangle(Color.White, (Program._width + 2) * Program._length - 10, Program._length - 5, Program._length * 3 + 20, Program._length * 3 + 15);
            SplashKit.FillRectangle(Color.White, (Program._width + 2) * Program._length - 10, Program._length * 5 - 15, Program._length * 3 + 20, Program._length * 3 + 25);
            SplashKit.DrawText("SCORE: " + _score.ToString(), Color.Black, (Program._width + 2) * Program._length, Program._length);
            SplashKit.DrawText("HIGHSCORE: " + _highscore.ToString(), Color.Black, (Program._width + 2) * Program._length, Program._length + 10);
            SplashKit.DrawText("NEXT BLOCK:", Color.Black, (Program._width + 2) * Program._length, Program._length + 20);
            SplashKit.DrawText("SAVED BLOCK:", Color.Black, (Program._width + 2) * Program._length, Program._length * 4 + 20);
            _nextTetromino.Draw();
            _tetromino.Draw();
            if (_savedTetromino != null){
                _savedTetromino.Draw();
            }

            if (_gameOver){
                SplashKit.FillRectangle(Color.White, (Program._length + Program._width * Program._length) / 2 - 25, (Program._length + Program._height * Program._length) / 2 - 10, 80, 20);
                SplashKit.DrawText("GAME OVER", Color.Black, (Program._length + Program._width * Program._length) / 2 - 20, (Program._length + Program._height * Program._length) / 2 - 5);
            }
        }

        public static Game Instance() {
            if (_instance == null) {
                _instance = new Game();
            }
            return _instance;
        }

        public void Rotate() {
            Block[] rotatedBlocks = _tetromino.rotatedBlocks();
            bool canRotate = true;
            foreach (Block block in rotatedBlocks) {
                if (block.X < 0 || block.X >= Program._width || block.Y < 0 || block.Y >= Program._height || _grid[block.X][block.Y].IsFull) {
                    canRotate = false;
                    break;
                }
            }

            if (canRotate) {
                _tetromino._blocks = rotatedBlocks;
            }
        }

        public Tetromino RandomTetromino(int x, int y){
            int shapeIndex = SplashKit.Rnd(0, 7);
            switch (shapeIndex){
                case 0: return new O(x,y);
                case 1: return new L(x,y);
                case 2: return new J(x,y);
                case 3: return new S(x,y);
                case 4: return new Z(x,y);
                case 5: return new T(x,y);
                case 6: return new I(x,y);
                default: return new T(x,y);
            }
        }

        public void AddTetromino() {
            _tetromino = _nextTetromino;
            _tetromino.Set(5, 0);
           _nextTetromino = RandomTetromino(Program._width + 2,1);
        }

        public void Run(){
            if (!_gameOver){
                Draw();
                int initialY = _tetromino._y;
                Move(0,1);
                if (initialY == _tetromino._y) {
                    Settle();
                    AddTetromino();
                }
            }
        }

        public void Move(int dx, int dy){
            bool blocked = false;
            foreach (Block b in _tetromino._blocks){
                if (b.X + dx < 0 || b.X + dx >= Program._width || b.Y + dy >= Program._height || _grid[b.X + dx][b.Y + dy].IsFull){
                    blocked = true;
                    break;
                }
            } if (!blocked){
                _tetromino.Move(dx,dy);
            }
        }

        public void Settle(){
            foreach (Block b in _tetromino._blocks){
                _grid[b.X][b.Y].Colour(_tetromino._color);
            }
            CheckAndClearRows();
            CheckAndClearRows();
            CheckAndClearRows();
            CheckAndClearRows();

            bool topRowTouched = false;
            for (int col = 0; col < Program._width; col++){
                if (_grid[col][0].IsFull){
                    topRowTouched = true;
                    break;
                }
            }

            if (topRowTouched){
                _gameOver = true;
                if (_score > _highscore){
                    SaveHighscore(_score);
                    _highscore = _score;
                }
            }
        }

        public void CheckAndClearRows(){
            for (int row = Program._height - 1; row >= 1; row--){
                bool rowFull = true;
                for (int col = 0; col < Program._width; col++){
                    if (!_grid[col][row].IsFull){
                        rowFull = false;
                        break;
                    }
                }

                if (rowFull){
                    for (int c = 0; c < Program._width; c++){
                        _grid[c][row].Clear();
                    }
                    for (int r = row - 1; r >= 0; r--){
                        for (int c = 0; c < Program._width; c++){
                            if (_grid[c][r].IsFull){
                                _grid[c][r + 1].Colour(_grid[c][r]._color);
                                _grid[c][r].Clear();
                            }
                        }
                    }
                    _score ++;
                }
            }
        }

        public void HoldTetromino() {
            if (_savedTetromino == null) {
                _savedTetromino = _tetromino;
                _savedTetromino.Set(Program._width + 2, 5);
                AddTetromino();
            } else {
                Tetromino temp = _tetromino;
                _tetromino = _savedTetromino;
                _tetromino.Set(5, 1);
                _savedTetromino = temp;
                _savedTetromino.Set(Program._width + 2, 5);
            }
        }

        public int GetHighscore() {
            StreamReader reader = new StreamReader("C:\\Users\\mamdo\\OneDrive\\Desktop\\mark\\C#\\tetris\\highscore.txt");
            int highscore;
            try {
                highscore = Convert.ToInt32(reader.ReadLine());
            } finally {
            reader.Close();
            }
            return highscore;
        }

        public void SaveHighscore(int highscore) {
            StreamWriter writer = new StreamWriter("C:\\Users\\mamdo\\OneDrive\\Desktop\\mark\\C#\\tetris\\highscore.txt");
            try {
                writer.WriteLine(highscore.ToString());
            } finally {
            writer.Close();
            }
        }
    }

    public class O : Tetromino{
        public O(int x, int y) : base(x, y) {
            _color = Color.Yellow;
            _blocks[0] = new Block(_x, _y, _color);
            _blocks[1] = new Block(_x + 1, _y, _color);
            _blocks[2] = new Block(_x, _y + 1, _color);
            _blocks[3] = new Block(_x + 1, _y + 1, _color);
        }
    }

    public class L : Tetromino{
        public L(int x, int y) : base(x, y) {
            _color = Color.Orange;
            _blocks[0] = new Block(_x - 1, _y + 1, _color);
            _blocks[1] = new Block(_x, _y + 1, _color);
            _blocks[2] = new Block(_x + 1, _y + 1, _color);
            _blocks[3] = new Block(_x + 1, _y, _color);
        }
    }

    public class J : Tetromino{
        public J(int x, int y) : base(x, y) {
            _color = Color.Indigo;
            _blocks[0] = new Block(_x - 1, _y, _color);
            _blocks[1] = new Block(_x - 1, _y + 1, _color);
            _blocks[2] = new Block(_x, _y + 1, _color);
            _blocks[3] = new Block(_x + 1, _y + 1, _color);
        }
    }

    public class S : Tetromino{
        public S(int x, int y) : base(x, y) {
            _color = Color.Green;
            _blocks[0] = new Block(_x, _y, _color);
            _blocks[1] = new Block(_x, _y + 1, _color);
            _blocks[2] = new Block(_x + 1, _y, _color);
            _blocks[3] = new Block(_x - 1, _y + 1, _color);
        }
    }

    public class Z : Tetromino{
        public Z(int x, int y) : base(x, y) {
            _color = Color.Red;
            _blocks[0] = new Block(_x - 1, _y, _color);
            _blocks[1] = new Block(_x, _y, _color);
            _blocks[2] = new Block(_x, _y + 1, _color);
            _blocks[3] = new Block(_x + 1, _y + 1, _color);
        }
    }

    public class I : Tetromino{
        public I(int x, int y) : base(x, y) {
            _color = Color.LightBlue;
            _blocks[0] = new Block(_x + 2, _y, _color);
            _blocks[1] = new Block(_x - 1, _y, _color);
            _blocks[2] = new Block(_x, _y, _color);
            _blocks[3] = new Block(_x + 1, _y, _color);
        }
    }

    public class T : Tetromino{
        public T(int x, int y) : base(x, y) {
            _color = Color.Purple;
            _blocks[0] = new Block(_x, _y, _color);
            _blocks[1] = new Block(_x - 1, _y, _color);
            _blocks[2] = new Block(_x + 1, _y, _color);
            _blocks[3] = new Block(_x, _y + 1, _color);
        }
    }
}