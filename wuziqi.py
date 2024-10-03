import tkinter as tk  # 导入 tkinter 库，创建图形界面。
from tkinter import messagebox

class wuziqi:  # 定义一个名为 "wuziqi" 的类，表示我们的五子棋游戏。
    def __init__(self, gamewindow, board_size=15):  # 初始化这个类，接受两个参数：一个窗口和棋盘的大小（默认是 15）。
        self.windowname = gamewindow  # 把传进来的窗口对象保存起来，以后会在这个窗口上显示东西。
        self.windowname.title("五子棋")  # 设置窗口的标题，告诉大家这个窗口是做什么的，名字叫“五子棋”。
        self.board_size = board_size  # 保存棋盘的大小，这个数字决定了棋盘的行和列。
        # 创建一个棋盘，用一个大小为 board_size 的列表表示，每个位置初始为空（表示没有棋子）。
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        # 创建一个同样大小的列表，用来存放每个棋子对应的按钮，初始时按钮都为空。
        self.buttons = [[None for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'X'  # 初始时让 'X' 先下，表示现在是 'X' 的回合。
        self.create_board()  # 调用创建棋盘的方法，开始显示棋盘上的按钮。

    def create_board(self):  # 创建棋盘的按钮
        for i in range(self.board_size):  # 先从0到棋盘的大小遍历每一行。
            for j in range(self.board_size):  # 然后再遍历每一列。
                # 创建一个按钮，初始时按钮的文本是空的，按钮的大小由 width 和 height 决定。
                # 点击这个按钮时会调用 on_click 方法，传入当前的行号和列号。
                button = tk.Button(self.windowname, text=' ', width=6, height=2,
                                   command=lambda i=i, j=j: self.on_click(i, j))
                # 把创建的按钮放到棋盘上，指定它的位置。
                button.grid(row=i, column=j)
                # 保存这个按钮到按钮列表中，这样我们以后可以访问这个按钮。
                self.buttons[i][j] = button

    def on_click(self, row, col):  # 当按钮被点击时，会执行这个方法，来处理点击事件
        # 检查被点击的按钮是否是空的，并且没有玩家已经赢了。
        if self.buttons[row][col]['text'] == ' ' and not self.is_winner():
            # 在棋盘上记录当前玩家下的棋子。
            self.board[row][col] = self.current_player  
            # 更新这个按钮的文本，显示当前玩家（是 'X' 还是 'O'）。
            self.buttons[row][col]['text'] = self.current_player  
            # 检查这个玩家是否赢了。
            if self.is_winner():
                # 如果赢了，就弹出一个窗口，告诉大家谁赢了。
                messagebox.showinfo("游戏结束", f"玩家 {self.current_player} 胜利！")
                self.reset_game()  # 重置游戏为下一局
            else:
                # 如果没有人赢，就切换到另一个玩家。
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def is_winner(self):  # 检查是否有玩家获胜的方法
        """检查当前棋盘上，是否有玩家已经获胜."""
        # 检查每一行
        for row in self.board:  # 遍历棋盘的每一行
            # 把这一行的内容变成一个字符串，检查里面是否有五个 'X' 或五个 'O' 连在一起。
            if 'XXXXX' in ''.join(row) or 'OOOOO' in ''.join(row):
                return True  # 找到五个相同的棋子就返回 True，表示有玩家赢了。

        # 检查每一列
        for col in range(self.board_size):  # 遍历棋盘的每一列
            # 收集这一列的所有棋子，放进一个列表里。
            column = [self.board[row][col] for row in range(self.board_size)]
            # 把这一列的内容变成一个字符串，检查里面是否有五个相同的棋子。
            if 'XXXXX' in ''.join(column) or 'OOOOO' in ''.join(column):
                return True  # 找到五个相同的棋子就返回 True。

        # 从左边界的每一行出发，检查正对角线 (从左上到右下)
        for row in range(self.board_size - 4):  # 确保至少有5个棋子可以连成一线
            diag = []  # 用来存储当前对角线上的棋子
            for i in range(self.board_size - row):  # 对角线最大长度为 board_size - row
                diag.append(self.board[row + i][i])  # 行列同步增长，形成正对角线
            if 'XXXXX' in ''.join(diag) or 'OOOOO' in ''.join(diag):  # 检查五子连珠
                return True

        # 从上边界的每一列出发，检查正对角线 (从左上到右下)
        for col in range(1, self.board_size - 4):  # 确保至少有5个棋子可以连成一线
            diag = []  # 用来存储当前对角线上的棋子
            for i in range(self.board_size - col):  # 对角线最大长度为 board_size - col
                diag.append(self.board[i][col + i])  # 行列同步增长，形成正对角线
            if 'XXXXX' in ''.join(diag) or 'OOOOO' in ''.join(diag):  # 检查五子连珠
                return True

        # 从左边界的每一行出发，检查反对角线 (从右上到左下)
        for row in range(self.board_size - 4):  # 确保至少有5个棋子可以连成一线
            diag = []  # 用来存储当前对角线上的棋子
            for i in range(self.board_size - row):  # 对角线最大长度为 board_size - row
                diag.append(self.board[row + i][self.board_size - 1 - i])  # 行增加，列减少，形成反对角线
            if 'XXXXX' in ''.join(diag) or 'OOOOO' in ''.join(diag):  # 检查五子连珠
                return True

        # 从下边界的每一列出发，检查反对角线 (从右上到左下)
        for col in range(1, self.board_size - 4):  # 确保至少有5个棋子可以连成一线
            diag = []  # 用来存储当前对角线上的棋子
            for i in range(self.board_size - col):  # 对角线最大长度为 board_size - col
                diag.append(self.board[i][self.board_size - 1 - (col + i)])  # 行增加，列减少，形成反对角线
            if 'XXXXX' in ''.join(diag) or 'OOOOO' in ''.join(diag):  # 检查五子连珠
                return True

        return False  # 如果找不到胜利的条件，返回 False，表示没有玩家赢。

    def reset_game(self):  # 这个方法用于重置游戏状态，准备下一局 '    o   x     '
        for i in range(self.board_size):  # 遍历棋盘的行
            for j in range(self.board_size):  # 遍历棋盘的列
                self.buttons[i][j]['text'] = ' '  # 清空按钮上的文本，恢复到初始状态
                self.board[i][j] = ' '  # 重置棋盘上这个位置的状态为空，表示没有棋子
        self.current_player = 'X'  # 将当前玩家重置为 'X'，也就是说重新开始这局游戏，X 先下

if __name__ == "__main__":  # 这行代码检查程序是否是直接运行的
    gamewindow = tk.Tk()  # 创建一个新的窗口，作为游戏的主界面
    game = wuziqi(gamewindow)  # 创建一个新的五子棋游戏对象，并把窗口传入
    gamewindow.mainloop()  # 启动窗口的主循环，等待用户的操作（比如点击按钮）
