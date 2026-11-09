# horse_tours/management/commands/generate_tour_docs.py
import os
from django.core.management.base import BaseCommand
from docx import Document

class Command(BaseCommand):
    help = 'Генерирует официальную Word-документацию проекта конного стартапа'

    def handle(self, *args, **options):
        doc = Document()
        
        doc.add_heading('Документация стартапа "Конные Туры" (Horse Tours Startup)', level=0)
        
        # Раздел 1. Архитектура и связи
        doc.add_heading('1. Архитектура моделей и DB-связей', level=1)
        doc.add_paragraph(
            '• 1-к-1 (One-to-One / Unique Slot): 1 человек может забронировать только 1 слот на фиксированные дату и время (Booking.unique_together).\n'
            '• 1-ко-многим (One-to-Many): 1 человек может оставлять несколько комментариев к турам (Comment.user -> User).\n'
            '• Многие-ко-многим (Many-to-Many): У тура может быть несколько категорий ("Конный", "Пеший", "На мото"), и одна категория принадлежит многим турам (Tour.categories).'
        )

        # Раздел 2. Код тестов
        doc.add_heading('2. Модульные тесты (horse_tours/tests.py)', level=1)
        tests_path = os.path.join('horse_tours', 'tests.py')
        
        if os.path.exists(tests_path):
            with open(tests_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            p = doc.add_paragraph()
            run = p.add_run(code_content)
            run.font.name = 'Courier New'
        else:
            doc.add_paragraph('Файл тестов не найден.')

        output_filename = 'Horse_Tours_Startup_Documentation.docx'
        doc.save(output_filename)
        self.stdout.write(self.style.SUCCESS(f'Документация успешно создана: {output_filename}'))