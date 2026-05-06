extends Node3D

var score: int = 0

func add_score(points: int):
	score += points
	print("AKTUALNY WYNIK: ", score)
