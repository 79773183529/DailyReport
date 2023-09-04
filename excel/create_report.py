import datetime
from openpyxl import load_workbook
from entities.task import Contractor


def create_report(filename, task_list):
    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    filename_copy = filename[:-5] + '_' + dt + '.xlsx'

    wb = load_workbook(filename)
    sheet = wb.active

    row = 6
    number = 1
    for task in task_list:
        sheet[f'A{row}'] = number
        sheet[f'B{row}'] = task.work_name.text
        sheet[f'C{row}'] = task.number_of_persons
        sheet[f'D{row}'] = eval(task.contractor).value
        sheet[f'E{row}'] = task.work_name.unit
        sheet[f'F{row}'] = task.work_name.volume
        sheet[f'G{row}'] = f"{task.work_name.done - task.completed}%"
        sheet[f'H{row}'] = f"{task.completed}%"
        sheet[f'I{row}'] = f"{task.work_name.done}%"

        row += 1
        number += 1

    wb.save(filename_copy)
    return filename_copy
