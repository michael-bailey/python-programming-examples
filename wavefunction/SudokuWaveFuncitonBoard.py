'''
	SudokuWaveFuncitonBoard.py
'''

from typing import Any, List, Tuple
import SudokuBoard
import SudokuBoardDelegate
import SudokuCellSuperposition


class SudokuWaveFuncitonBoard(SudokuBoardDelegate.SudokuBoardDelegate):

	__array: List[List['SudokuCellSuperposition.SudokuCellSuperposition']]

	__rows: List[List['SudokuCellSuperposition.SudokuCellSuperposition']]
	__cols: List[List['SudokuCellSuperposition.SudokuCellSuperposition']]
	__squares: List[List['SudokuCellSuperposition.SudokuCellSuperposition']]

	def __init__(self) -> None:
		super().__init__()
		# create array for holding all values
		self.__array = [[SudokuCellSuperposition.SudokuCellSuperposition() for _ in range(1,10)] for _ in range(1,10)]

		# create arrays for each
		self.__rows = [x for x in self.__array]
		self.__cols = [[i[row] for i in self.__array] for row in range(0, 9)]
		self.__squares = chunk(self.__array)
		for row in self.__rows:
			for element in row:
				element.row = row
		
		for col in self.__cols:
			for element in col:
				element.col = col

		for squ in self.__squares:
			for element in squ:
				element.square = squ


	def cell_update(self, board: 'SudokuBoard.SudokuBoard', row: int, col: int):
		print("[SudokuWaveFuncitonBoard:cell_update] row:{} col:{}".format( row,col))
		number = board.array[row][col]
		self.collapse(row, col, number)
		
		for (r_index, t_row) in enumerate(self.__array):
			for (c_index, el) in enumerate(t_row):
				if el.value == None: continue
				board.array[r_index][c_index] = el.value

	def init_update(self, board: 'SudokuBoard.SudokuBoard'):
		print("[SudokuWaveFuncitonBoard:init_update]")
		for (r_index, row) in enumerate(board.array):
			for (c_index, col) in enumerate(row):
				match col:
					case "_":
						continue
					case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
						self.collapse(r_index,c_index, col)
						
	def collapse(self, row: int, col: int, number: str):
		self.__array[row][col].collapse(number)

	def get_lowest_entropys(self) -> List[Tuple['SudokuCellSuperposition.SudokuCellSuperposition', int, int]]:
		lowest_list: List[Tuple['SudokuCellSuperposition.SudokuCellSuperposition', int, int]] = []
		lowest_value = 10

		for (r_index, row) in enumerate(self.__array):
			for (c_index, element) in enumerate(row):
				if element.is_collapsed(): continue
				ent = element.get_entropy()
				if ent < lowest_value:
					lowest_list = [(element, r_index, c_index)]
					lowest_value = ent
				elif ent == lowest_value:
					lowest_list.append((element, r_index, c_index))
		return lowest_list


def chunk(arr: List[List[Any]]) -> List[List[Any]]:
	chunks = [[row[i:i + 3] for i in range(0, len(row), 3)] for row in arr]
	final = []

	for i in range(0,len(chunks), 3):
		cur = [[],[],[]]
		for j in chunks[i:i+3]:
			cur[0].extend(j[0])
			cur[1].extend(j[1])
			cur[2].extend(j[2])
		final.extend(cur)
	return final
