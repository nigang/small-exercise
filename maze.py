# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 16:55:09 2018

@author: gni
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 14:27:54 2018

@author: gni
"""

import sys, queue
from PyQt5 import QtCore, QtGui, QtWidgets


class ElemMarker():
    def __init__(self,i,j):
        self.row = i
        self.column = j
        self.visited = 0
        self.obstacle = False

 
class MazeThread(QtCore.QThread):
    visited_signal = QtCore.pyqtSignal(int, int, int, int)
    shortest_path_signal = QtCore.pyqtSignal(list)

    def __init__(self, dimension):
        super(MazeThread, self).__init__()
        self.dimension = dimension
        self.distance = [[ -1 for i in range(self.dimension)] for j in range(self.dimension)]
        self.maze_array = [[ElemMarker(j,i) for i in range(self.dimension)] for j in range(self.dimension)]
        self.methodology = None
        self.min_step = 0
        
    def set_obstacle(self, row, column, isTrue):
        if isTrue:
            self.maze_array[row][column].obstacle = True
        else:
            self.maze_array[row][column].obstacle = False
        
    def resume_visited(self):        
        for row in range(self.dimension):
            for column in range(self.dimension):
                if not self.maze_array[row][column].obstacle:
                    self.maze_array[row][column].visited = 0
               
    def run(self):
        self.resume_visited()
        if self.methodology == "BFS":
            self.shortest_path_bfs()
        elif self.methodology == "DFS":
            self.shortest_path_dfs()
        else:
            pass
        
    def set_visited(self, ele, add_=True):
        if add_:
            ele.visited += 1
        self.visited_signal.emit(ele.row, ele.column, ele.visited, self.distance[ele.row][ele.column])
        self.msleep(50)
        
    def set_unvisited(self, ele):
        ele.visited = 0
        self.visited_signal.emit(ele.row, ele.column, 0, self.distance[ele.row][ele.column])
        
    def find_neighbor_btn(self, ele):
        
        neighbor_list = list()
        row = ele.row
        column = ele.column
        dimension = self.dimension
        
        if row + 1 <= dimension-1 and not self.maze_array[row+1][column].obstacle:
            neighbor_list.append(self.maze_array[row+1][column])        
        if column + 1 <= dimension -1  and not self.maze_array[row][column+1].obstacle:
            neighbor_list.append(self.maze_array[row][column+1])             
        if column - 1 >= 0 and not self.maze_array[row][column -1].obstacle:
            neighbor_list.append(self.maze_array[row][column-1])            
        if row - 1 >= 0 and not self.maze_array[row-1][column].obstacle:
            neighbor_list.append(self.maze_array[row-1][column])
            
        return neighbor_list  
        
    def path_dfs(self, node):
        neighbor_list = self.find_neighbor_btn(node)
        for ele in neighbor_list :
            if ele.visited:
                self.set_visited(ele)
                if self.distance[ele.row][ele.column] > self.distance[node.row][node.column] + 1:
                    self.distance[ele.row][ele.column] = self.distance[node.row][node.column] + 1                    
                    self.set_visited(ele, add_ = False)
                    self.path_dfs(ele)   #update its neighbors
            else:
                self.distance[ele.row][ele.column] = self.distance[node.row][node.column] + 1
                self.set_visited(ele)
                self.path_dfs(ele)
                
    def path_dfs_x(self, node, dis):
        if dis > self.min_step:
            return
        elif node.row == self.dimension-1 and node.column == self.dimension -1:
            if self.min_step > dis:
                self.min_step = dis
            return
        neighbor_list = self.find_neighbor_btn(node)
        for ele in neighbor_list:            
            if not ele.visited:
                if self.distance[ele.row][ele.column] > dis + 1:
                    self.distance[ele.row][ele.column] = dis + 1
                self.set_visited(ele)
                self.path_dfs_x(ele, dis + 1)
                self.set_unvisited(ele)
                
    def shortest_path_dfs(self):  
        self.resume_visited()
        self.min_step = 1e19
        self.distance = [[1e19 for i in range(self.dimension)] for j in range(self.dimension)]
        source = self.maze_array[0][0]
        self.distance[source.row][source.column] = 0 
        self.set_visited(source)
        self.path_dfs_x(source,0)
        path_list = self.fetch_one_shortest_path()
        self.shortest_path_signal.emit(path_list)
        
    def shortest_path_bfs(self):
        self.resume_visited()
        self.distance = [[-1 for i in range(self.dimension)] for j in range(self.dimension)]
        source = self.maze_array[0][0]
        v_set = queue.Queue()
        v_set.put(source)
        self.distance[source.row][source.column] = 0
        self.set_visited(source)
        
        while not v_set.empty():
            cur_ele = v_set.get()
            neighbor_list = self.find_neighbor_btn(cur_ele)            
            for ele in neighbor_list:
##                if ele.visited:
##                    self.set_visited(ele)
##                    if self.distance[ele.row][ele.column] > self.distance[cur_ele.row][cur_ele.column] + 1:
##                        self.distance[ele.row][ele.column]  = self.distance[cur_ele.row][cur_ele.column] + 1 
##                        v_set.put(ele)
##                        self.set_visited(ele, add_ = False)
##                else:
                if not ele.visited:
                    self.distance[ele.row][ele.column] = self.distance[cur_ele.row][cur_ele.column] + 1
                    self.set_visited(ele)
                    v_set.put(ele)
        path_list = self.fetch_one_shortest_path()
        self.shortest_path_signal.emit(path_list) 
        
    def fetch_one_shortest_path(self):
        self.resume_visited()
        path_stack = list()
        shortest_steps = self.distance[self.dimension -1][self.dimension-1]
        if shortest_steps == -1:
            return
        via_ele = self.maze_array[self.dimension-1][self.dimension-1]
        via_ele.visited = 1
        path_stack.append(via_ele)
        
        while shortest_steps:
            neighbor_list = self.find_neighbor_btn(path_stack[-1])
            for ele in neighbor_list:
                if self.distance[ele.row][ele.column] + 1 == shortest_steps and not ele.visited:
                    path_stack.append(ele)
                    ele.visited = 1
                    shortest_steps -= 1
                    break
        return path_stack    


class MyButton(QtWidgets.QPushButton):    
    obstacle_signal = QtCore.pyqtSignal(int, int, bool)

    def __init__(self, row, column):
        super(MyButton, self).__init__()
        self.setStyleSheet("QPushButton{background-color:rgb(240,240,240)}")
        self.visited = 0
        self.setText("0 0")
        self.obstacle = False
        self.clicked.connect(self.set_obstacle)
        self.row = row
        self.column = column

    def set_obstacle(self):
        if not self.obstacle:
            self.obstacle = True
            self.setStyleSheet("QPushButton{background-color:black}")
            self.obstacle_signal.emit(self.row, self.column, True)
        else:
            self.obstacle = False            
            self.setStyleSheet("QPushButton{background-color:rgb(240,240,240)}")     
            self.obstacle_signal.emit(self.row, self.column, False)   
        self.update()
        
    def set_visited(self, counter, distance):
        self.visited = counter
        if counter == 0:
            self.setStyleSheet("QPushButton{background-color:rgb(240,240,240)}") 
        else:
            green = 220 - counter
            blue = 220 - counter 
            self.setStyleSheet("QPushButton{background-color:rgb(255,%d,%d)}"%(green, blue)) 
        self.setText("%d %d" % (counter, distance))
        self.update()
        
    def remove_result(self):
        if self.obstacle:
            self.setStyleSheet("QPushButton{background-color:black}")
        else:        
            self.setStyleSheet("QPushButton{background-color:rgb(240,240,240)}")
        self.setText("0 0")
        self.update()
        
    def show_path_on_self(self):
        self.setStyleSheet("QPushButton{background-color:rgb(255,170,0)}")
        self.update()


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.btn_array = list()
        self.main_layout = QtWidgets.QHBoxLayout()
        self.array_layout = QtWidgets.QGridLayout()

        self.btn_config_layout = QtWidgets.QHBoxLayout()
        
        self.show_btn = QtWidgets.QPushButton("Show Maze")
        self.dfs_btn = QtWidgets.QPushButton("dfs")
        self.show_result_btn = QtWidgets.QPushButton("Result")
        self.show_result_btn.setEnabled(False)
        self.bfs_btn = QtWidgets.QPushButton("bfs")
        self.txt_line = QtWidgets.QLineEdit() 
        
        self.btn_config_layout.addWidget(self.txt_line)
        self.btn_config_layout.addWidget(self.show_btn)

        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_layout.addLayout(self.btn_config_layout)
        self.main_layout.addLayout(self.array_layout)
        self.main_layout.addLayout(self.right_layout)

        self.right_layout.addWidget(self.bfs_btn)
        self.right_layout.addWidget(self.dfs_btn)
        self.right_layout.addWidget(self.show_result_btn)
        
        self.setLayout(self.main_layout)
        self.main_layout.addStretch( )
        self.path = list()
        self.maze_thread = None
        self.color = [(170,255,0),(0,255,0),(255,0,0),(0,0,255),(170,0,255),(0,170,255),(85,85,0),(85,170,255),(255,0,255),(255,170,0)]
        self.show_btn.clicked.connect(self.show_array)
        self.show_result_btn.clicked.connect(self.show_result)
        self.bfs_btn.clicked.connect(self.shortest_path_bfs)
        self.dfs_btn.clicked.connect(self.shortest_path_dfs)
        self.dimension = 0

    def show_result(self):
        for ele in self.path:
            self.btn_array[ele.row][ele.column].show_path_on_self()
        self.setEnabled(True)
        self.dfs_btn.setEnabled(True)
        self.bfs_btn.setEnabled(True)
        
    def shortest_path_bfs(self):
        self.bfs_btn.setEnabled(False)
        self.setEnabled(False)
        self.show_result_btn.setEnabled(False)
        self.maze_thread.terminate()
        self.remove_result()
        self.maze_thread.methodology = "BFS"
        self.maze_thread.start()
    
    def shortest_path_dfs(self):
        self.dfs_btn.setEnabled(False)
        self.setEnabled(False)
        self.show_result_btn.setEnabled(False)
        self.maze_thread.terminate()
        self.remove_result()
        self.maze_thread.methodology = "DFS"
        self.maze_thread.start()

    def set_visited(self, row, column, counter,distance):
        self.btn_array[row][column].set_visited(counter,distance)
        
    def setEnabled(self, is_enabled):
        for row in range(self.dimension):
            for column in range(self.dimension):
                self.btn_array[row][column].setEnabled(is_enabled)
        self.update()
        
    def remove_result(self):        
        self.path = list()
        for row in range(self.dimension):
            for column in range(self.dimension):
                self.btn_array[row][column].remove_result()

    def show_path(self, l):
        self.path = l
        self.show_result_btn.setEnabled(True)
        self.update()
        
    def show_array(self):
        self.dfs_btn.setEnabled(True)
        self.bfs_btn.setEnabled(True)
        try:
            self.dimension = (int (self.txt_line.text()))
            if self.dimension <= 1:
                raise ValueError
        except ValueError:
            QtWidgets.QMessageBox.about(self, "Error","Need a positive integer greater than 1")
            return
            
        if self.maze_thread:
            self.maze_thread.terminate()
        self.maze_thread = MazeThread(self.dimension)
        self.maze_thread.visited_signal.connect(self.set_visited)
        self.maze_thread.shortest_path_signal.connect(self.show_path)
        dimension = self.dimension
        self.txt_line.clear()
        
        for row in self.btn_array:
            for btn in row:
                self.array_layout.removeWidget(btn)
                btn.setVisible(False)
                
        self.btn_array =   [ [None for i in range(dimension)] for j in range(dimension)] 
        
        for row in range(dimension):
            for column in range(dimension):
                btn = MyButton(row,column)
                btn.obstacle_signal.connect(self.maze_thread.set_obstacle)
                self.btn_array[row][column] = btn
                self.array_layout.addWidget(self.btn_array[row][column], row, column)
        self.array_layout.setSpacing(0)
        self.update()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
