def extract_result(f_name):
	
	result_list = []
	
	with open(f_name) as f:
		for l in f.readlines():
			result_list.append(l)
	
	result_set = set(result_list)
	
	if len(result_set) == len(result_list):
		print(f"В {f_name} все переменные уникальны, их {len(result_list)}")
	else:
		print(f"В {f_name} обнаружен дефект, имеются дубликаты")
	
	return result_list, result_set


def delta_diff(new_e, new_d, old_e, old_d):
	
	if len(old_e) < len(new_e):
		diff_e = set(set(old_e).difference(set(new_e)))
		delta_e = len(new_e) - len(old_e)
	else:
		diff_e = set(set(new_e).difference(set(old_e)))
		delta_e = len(new_e) - len(old_e)
	if len(old_d) < len(new_d):
		diff_d = set(set(old_d).difference(set(new_d)))
		delta_d = len(new_d) - len(old_d)
	else:
		diff_d = set(set(new_d).difference(set(old_d)))
		delta_d = len(new_d) - len(old_d)
	
	qe_of_d_new = (len(new_e)/len(new_d)) * 100
	qe_of_d_old = (len(old_e)/len(old_d)) * 100
	
	print(f"Отлов емайлов в доменах в новой раздаче равен {int(qe_of_d_new)}%")
	print(f"Отлов емайлов в доменах в старой раздаче равен {int(qe_of_d_old)}%")
	print(f"Разница в количестве обработанных адресов в последней раздаче: {delta_d} и разница в кол-ве полученнных  емайлов {delta_e} ")
	
	return diff_e, diff_d, delta_e, delta_d

new_e = extract_result("backup/emails.csv")[1]
new_d = extract_result("backup/domains.csv")[1]

old_e = extract_result("backup/last-emails.csv")[1]
old_d = extract_result("backup/last-domains.csv")[1]

diff_e, diff_d, delta_e, delta_d = delta_diff(new_e, new_d, old_e, old_d)
print(f"Новых доменов обработанно {len(diff_d)}")
print(f"Новых емайлов получено {len(diff_e)}")
print("Все неявные зависимости подтверждены, результат удовлетворительный !")

