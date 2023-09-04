from entities.work_name import WorkName, Category
from data_base.with_db import add_new_work_name

work_names: list[WorkName] = [
    WorkName(
        text="Монтаж каркаса для ГКЛ(металлоконструкции над витражами)",
        category=Category.FINISHING,
        unit="м2",
        volume=78.00,
        done=72.00
    ),
    WorkName(
        text="Обшивка перегородок и стен листами ГКЛ",
        category=Category.FINISHING,
        unit="м2",
        volume=1297.00,
        done=55.00
    ),
    WorkName(
        text="Монтаж металлоконструкций под кладку из газоблока",
        category=Category.FINISHING,
        unit="м",
        volume=12,
        done=93
    ),
    WorkName(
        text="Покраска металлоконструкций под витражи",
        category=Category.FINISHING,
        unit="тн",
        volume=12.4,
        done=86.00
    ),
    WorkName(
        text="Изготовление металлоконструкций под  наружные витражи",
        category=Category.METAL,
        unit="тн",
        volume=17.00,
        done=93.00
    ),
    WorkName(
        text="Монтаж металлоконструкций под  наружные витражи",
        category=Category.METAL,
        unit="тн",
        volume=17.00,
        done=72.00
    ),
    WorkName(
        text="Разнорабочие (Уборка территории)",
        category=Category.FINISHING,
        unit=" ",
        volume=0.00,
        done=0.00
    ),
    WorkName(
        text="Шумоизоляция венткамеры 1",
        category=Category.FINISHING,
        unit="м2",
        volume=132.00,
        done=90.50
    ),
    WorkName(
        text="Шумоизоляция венткамеры 2",
        category=Category.FINISHING,
        unit="м2",
        volume=146.00,
        done=37.00
    ),
    WorkName(
        text="Устройство утепления и гидроизоляции цоколя",
        category=Category.ROOF,
        unit="м",
        volume=430.00,
        done=83.00
    ),
    WorkName(
        text="",
        category=Category.METAL,
        unit="м2",
        volume=17.00,
        done=93.00
    ),
    WorkName(
        text="Установка вентиляционного оборудования",
        category=Category.VENTILATION,
        unit="шт",
        volume=1.00,
        done=73.00
    ),
    WorkName(
        text="Монтаж системы кондиционирования. Медные трубы",
        category=Category.CONDITIONING,
        unit="м",
        volume=458.00,
        done=93.00
    ),
    WorkName(
        text="Монтаж  лотков под прокладку кабельных линий",
        category=Category.ELECTRICS,
        unit="м",
        volume=996.00,
        done=73.00
    ),
    WorkName(
        text="Монтаж кабельных линий системы СПЗ",
        category=Category.LOW_CURRENT,
        unit="м",
        volume=7144.00,
        done=34.00
    ),
    WorkName(
        text="Планировка грунта под благоустройство. Захватка 1 (вдоль оси 1)",
        category=Category.LANDSCAPING,
        unit="м2",
        volume=516.00,
        done=49.00
    ),
    WorkName(
        text="Устроойство щебёночного основания. Захватка 1 (вдоль оси 1)",
        category=Category.LANDSCAPING,
        unit="м2",
        volume=516.00,
        done=34.00
    ),
    WorkName(
        text="Малярные работы венткамера 2",
        category=Category.FINISHING,
        unit="м2",
        volume=146.00,
        done=64.00
    ),
    WorkName(
        text="Малярные работы венткамера 1",
        category=Category.FINISHING,
        unit="м2",
        volume=164.00,
        done=0.00
    ),
    WorkName(
        text="Укладка плитки керамогранит 600*1200",
        category=Category.FINISHING,
        unit="м2",
        volume=2020.00,
        done=69.00
    ),
    WorkName(
        text="Устройство колодцев в уровень благоустройства",
        category=Category.PLUMBING,
        unit="шт",
        volume=16,
        done=60.00
    ),
    WorkName(
        text="Малярные работы по стенам",
        category=Category.FINISHING,
        unit="м2",
        volume=4240.00,
        done=29.00
    ),
    WorkName(
        text="Штукатурные работы по стенам",
        category=Category.FINISHING,
        unit="м2",
        volume=348.00,
        done=29.00
    ),
    WorkName(
        text="Планировка грунта под благоустройство. Захватка 2 (вдоль оси а)",
        category=Category.LANDSCAPING,
        unit="м2",
        volume=458.00,
        done=80.00
    ),
    WorkName(
        text="Монтаж дренажной системы",
        category=Category.PLUMBING,
        unit="м2",
        volume=1.00,
        done=13.00
    ),
    WorkName(
        text="Устройство наливного пола",
        category=Category.FINISHING,
        unit="м2",
        volume=2130.00,
        done=44.00
    ),
    WorkName(
        text="Монтаж утеплителя Пеноплекс на кровлю",
        category=Category.ROOF,
        unit="м3",
        volume=226.00,
        done=55.00
    ),
    WorkName(
        text="Монтаж ПВХ мембраны",
        category=Category.ROOF,
        unit="м2",
        volume=3419.00,
        done=14.00
    ),
    WorkName(
        text="Прокладка кабельных линий",
        category=Category.ELECTRICS,
        unit="м",
        volume=32808.00,
        done=19.00
    ),
    WorkName(
        text="Малярные работы по ЛМ-2",
        category=Category.FINISHING,
        unit="м2",
        volume=330.00,
        done=21.00
    ),
    WorkName(
        text="Устройство  ЖБ лотков",
        category=Category.LANDSCAPING,
        unit="м3",
        volume=27.00,
        done=93.00
    ),
    WorkName(
        text="Устройство бордюрного камня",
        category=Category.LANDSCAPING,
        unit="м",
        volume=1177.00,
        done=10.00
    ),
    WorkName(
        text="Устройство тротуарной плитки",
        category=Category.LANDSCAPING,
        unit="м2",
        volume=1669.00,
        done=3.00
    ),
    WorkName(
        text="Монтаж кронштейнов",
        category=Category.FACADE,
        unit="шт",
        volume=7712.00,
        done=10.00
    ),
    WorkName(
        text="Монтаж минераловатного утеплителя по фасаду",
        category=Category.FACADE,
        unit="м3",
        volume=265.00,
        done=11.00
    ),
    WorkName(
        text="Монтаж кабельных линий системы СС",
        category=Category.LOW_CURRENT,
        unit="м",
        volume=17607.00,
        done=49.00
    ),
    WorkName(
        text="Устройство плитки напольной в венткамере",
        category=Category.FINISHING,
        unit="м",
        volume=160.00,
        done=60.00
    ),
    WorkName(
        text="Монтаж каркасов наружных витражей и  окон",
        category=Category.EXTERIOR_GLAZING,
        unit="м2",
        volume=814.00,
        done=81.00
    ),
    WorkName(
        text="Бригадир",
        category=Category.ELECTRICS,
        unit="шт",
        volume=0.00,
        done=0.00
    ),
    WorkName(
        text="Бригадир",
        category=Category.FINISHING,
        unit="шт",
        volume=0.00,
        done=0.00
    ),
    WorkName(
        text="Дежурный электрик",
        category=Category.ELECTRICS,
        unit="шт",
        volume=0.00,
        done=0.00
    ),
]


for work_name in work_names:
    add_new_work_name(work_name)

