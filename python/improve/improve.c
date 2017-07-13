//コンパイル時に -lmオプションを付ける(exp関数を使っているため)
/*
 今後改良できる点
 ・評価関数の特徴量を増やす
 ・重みベクトルを別ファイルに保存できるようにする
 ・強くなったどうかを対戦によって確かめる(あるいは，対戦ではなく，多数回対戦させて統計的な手法によって確かめる)
 */
/*
 こちらのimprove.cでは，適切な重み関数の値を求めることにする。
 50個目の石が置かれるまではnmovesで評価する。
 */

#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

typedef struct 
{
  int first;
  int second;
} IntPair;

IntPair directions[8] = {
  { -1, -1 }, {  0, -1 }, { 1, -1 }, 
  { -1,  0 },             { 1,  0 }, 
  { -1,  1 }, {  0,  1 }, { 1,  1 } 
};

int board[8][8];

#define NUM_FEATURES 11 //普通，角，中央，角の隣
double weight[NUM_FEATURES] = {100, 653.0, -130.4, -66.6, -56.2, -44.8, -306.7, -135.6, -151.2, -1150.0, -2340.2}; // weights of the features
int last_stage=4; //石がlast_stage個以上なら終盤と判断する

//initialize
void init_board()
{
  int c, r; // column, row
  for (r = 0; r < 8; r++) 
    for (c = 0; c < 8; c++)
      board[c][r] = 0;

  board[4][3] = board[3][4] =  1;  // black disks
  board[3][3] = board[4][4] = -1;  // white disks
}

void print_board()
{
  int c, r;
  puts("\n  a b c d e f g h");
  for (r = 0; r < 8; r++) {
    printf("%d", r + 1);
    for (c = 0; c < 8; c++) {
      const int d = board[c][r];
      char s = '.';
      if (d ==  1) s = 'B'; // black disk
      if (d == -1) s = 'W'; // white disk
      printf(" %c", s);
    }
    putchar('\n');
  }
    putchar('\n');
}

//sqからみてdirの方向に挟める石があるかどうか見る(あるなら1)
int can_flip(const int side, 
             IntPair sq, const IntPair dir) // square, direction
{
  assert(board[sq.first][sq.second] == 0); //stop the program if false　sqには石が必ずある
  int n = 0;
  do {
    sq.first  += dir.first; 
    sq.second += dir.second; //move the stone
    n++;
    if (sq.first < 0 || sq.first >= 8 || sq.second < 0 || sq.second >= 8) return 0;
  } while (board[sq.first][sq.second] == -side); //if it has an opponent's stone
  if (board[sq.first][sq.second] == 0) return 0; //if there is no stone in the square, return 0
  if (n <= 1) return 0; //隣り合って同じ色の石が
  return 1;
}

//sqに石が置けるかどうか見る
int is_legal_move(int side, IntPair sq)
{
  assert(sq.first >= 0 && sq.first < 8 && sq.second >= 0 && sq.second < 8); //see if it's on board first of all
  int i;
  if (board[sq.first][sq.second] != 0) return 0;
  for (i = 0; i < 8; i++) {
    if (can_flip(side, sq, directions[i])) return 1; //各方面について
  }
  return 0;
}

//石を置く，あるいはひっくり返す
int place_disk(const int side, const IntPair sq)
{
  assert(is_legal_move(side, sq)); //sqに石が置けないならプログラム停止
  int n = 0, i;
  for (i = 0; i < 8; i++) {
    const IntPair dir = directions[i];
    if (!can_flip(side, sq, dir)) continue; //？？
    int c = sq.first  + dir.first;
    int r = sq.second + dir.second;
    while (board[c][r] == -side) { //相手の石があればひっくり返す
      board[c][r] = side;
      n++;
      c += dir.first;
      r += dir.second;
    }
  }
  board[sq.first][sq.second] = side; //置いた所も自分の色に
  assert(n > 0);
  return n; //何枚ひっくり返せたか
}

int generate_legal_moves(const int side, IntPair legal_moves[60])
{
  int c, r, nmoves = 0, nempty = 0;
  for (c = 0; c < 8; c++) {
    for (r = 0; r < 8; r++) {
      if (board[c][r] != 0) continue; //マスが埋まっていたら続ける
      nempty++; //nemptyは埋まっているマスの数
      IntPair sq;
      sq.first = c; sq.second = r;
      if (!is_legal_move(side, sq)) continue;
      assert(nmoves < 60);
      legal_moves[nmoves++] = sq; //legal_movesの中に合法手を保存
    }
  }
  if (nempty == 0) return -1;
  return nmoves; //合法手の数
}

int count_disks()
{
  int sum = 0;
  int c, r;
  for (c = 0; c < 8; c++) {
    for (r = 0; r < 8; r++) {
      sum += board[c][r];
    }
  }
  return sum;
}

//黒い石の数
int feature(int id)
{
    int total = 0, c, r;
    switch(id){
        case 0:
            for (c = 0; c < 8; c++) {
                for (r = 0; r < 8; r++) {
                    total += board[c][r];
                }
            }
            return total;
            break;

        case 1:
            return board[0][0] + board[0][7] + board[7][0] + board[7][7];

        case 2:
            return board[3][3] + board[3][4] + board[4][3] + board[4][4];
            
        case 3:
            return board[1][0] + board[6][0] + board[0][1] + board[7][1] + board[0][6] + board[7][6] + board[1][7] + board[6][7];

        case 4:
            return board[0][2] + board[0][5] + board[2][0] + board[2][7] + board[5][0] + board[5][7] + board[7][2] + board[7][5];

        case 5:
            return board[0][3] + board[0][4] + board[3][0] + board[3][7] + board[4][0] + board[4][7] + board[7][3] + board[7][4];

        case 6:
            return board[1][1] + board[1][6] + board[6][1] + board[6][6];

        case 7:
            return board[1][2] + board[1][5] + board[2][1] + board[2][6] + board[5][1] + board[5][6] + board[6][2] + board[6][5];

        case 8:
            return board[1][3] + board[1][4] + board[3][1] + board[3][6] + board[4][1] + board[4][6] + board[6][3] + board[6][4];
            
        case 9:
            return board[2][2] + board[2][5] + board[5][2] + board[5][5];

        case 10:
            return board[2][3] + board[2][4] + board[3][2] + board[3][5] + board[4][2] + board[4][5] + board[5][3] + board[5][4];

        default:
            exit(1);
    }
}

//評価関数
int evaluate(int turn)
{
    int nstones=64; //盤面の石の数
    int c,r;
    for(c = 0; c < 8; c++){
        for(r = 0; r < 8; r++){
            if(board[c][r] == 0) nstones--;
        }
    }
    
    if(nstones > last_stage){
        double score = 0;
        int i;
        for (i = 0; i < 9; i++) {
            score += feature(i) * weight[i];
        }
        return score;
    } else {
        IntPair legal_moves[60];
        return generate_legal_moves(-turn, legal_moves);
    }
}

int negamax(int depth, int max_depth, int turn, IntPair *best_move)
{
  if (depth == max_depth) {
    return turn * evaluate(turn);
  }

  IntPair legal_moves[60];
  const int nmoves = generate_legal_moves(turn, legal_moves);

  if (nmoves <= 0) {
    IntPair dummy;
    const int score = -negamax(depth + 1, max_depth, -turn, &dummy);
    return score;
  }

  int board0[8][8];
  memcpy(board0, board, 8*8*sizeof(int));

  int i;
  int best_score = -99999;
  for (i = 0; i < nmoves; i++) {
    const IntPair move = legal_moves[i];
    place_disk(turn, move);

    IntPair dummy;
    const int score = -negamax(depth + 1, max_depth, -turn, &dummy);
    if (depth == 0) {
      //printf("move = %c%c, score = %d\n",
	  //   'a' + move.first, '1' + move.second, score);
    }
    if (score > best_score) {
      *best_move = move;
      best_score = score;
    }
    memcpy(board, board0, 8*8*sizeof(int));
  }

  return best_score;
}

void selfplay()
{
    int ply_rec = rand() % 63; // The features will be recorded at this ply.
    double f[NUM_FEATURES]; // The values of the features
    double pb = -1; // P(Winner=Black) 黒が勝つ確率
    double a = 0.001; //スライドに出てくるaそのまま
    double learning_rate = 1000; //学習率(どのくらいの幅で移動するか)
    
    init_board();
    
    int turn;
    int pass[2] = { 0, 0 };
    int ply = 0;
    for (turn = 1;; turn *= -1, ply++) {
        
        IntPair legal_moves[60];
        const int nmoves = generate_legal_moves(turn, legal_moves);
        if (ply == ply_rec) {
            int i;
            for (i = 0; i < NUM_FEATURES; i++) {
                f[i] = feature(i);
            }
            pb = 1.0 / (1.0 + exp(-a*evaluate(turn)));
        }
        
        if (nmoves == -1) break;     // no empty square
        if (nmoves ==  0) {
            pass[(turn + 1)/2] = 1;
            if (pass[(-turn + 1)/2] == 1) break; // pass x 2
            continue;  // pass (no legal move)
        }
        pass[(turn + 1)/2] = 0;
        
        IntPair move;
        if (ply < ply_rec) move = legal_moves[rand() % nmoves];
        else               negamax(0, 3, turn, &move);
        place_disk(turn, move);
    }
    
    if (pb < 0) return;
    
    int d = count_disks();
    if (d == 0) return; //引き分けなら表示しない
    
    int i;
    printf("Winner=");
    if (d > 0) printf("Black");
    else       printf("White");
    printf(" pb = %.2f ", pb);
    
    for (i = 1; i < NUM_FEATURES; i++) { //iは1から(0番の重みは動かさない)
        //printf(", f[%d] = %.1f ", i, f[i]);

        //w[i]をアップデート
        if (d > 0) weight[i] += learning_rate * (1.0 - pb) * a * f[i]; //黒が勝ったとき
        else       weight[i] -= learning_rate * pb * a * f[i]; //白が勝ったとき
        printf("%.1f, ", weight[i]);
    }
    //printf("ply_rec = %d", ply_rec);
    printf("\n");
}

int main(int argc, char **argv)
{
  srand(12345);
  const int human_side = (argc >= 2) ? atoi(argv[1]) : 0;

    int i;
    for (i = 0; i < 10000; i++) {
        selfplay();
    }
  exit(0);
}
