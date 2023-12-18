import os

from json import dumps
from argparse import ArgumentParser
from time import perf_counter

from TheMoscowTimes import TheMoscowTimes, helpers

def get_data(args) -> dict:
    tmt: TheMoscowTimes = TheMoscowTimes()

    if(not args.keyword): return tmt.get_by_category(category=args.category, page=args.page)
    
    return tmt.search(keyword=args.keyword, page=args.page, category=args.category, from_date=args.from_date, to_date=args.to_date)


if(__name__ == '__main__'):
    argp: ArgumentParser = ArgumentParser()
    argp.add_argument("--category", '-c', type=str, default='news')
    argp.add_argument("--page", '-p', type=int, default=1)
    argp.add_argument("--keyword", '-k', type=str, default=None)
    argp.add_argument("--from_date", '-fd', type=str, default=None)
    argp.add_argument("--to_date", '-td', type=str, default=None)
    argp.add_argument("--output", '-o', type=str, default='data')
    args = argp.parse_args()

    helpers.logging.info('Start crawling...')
    start = perf_counter()

    data: dict = get_data(args=args)

    if(not os.path.exists(args.output)):
        os.makedirs(args.output)

    with open(f'{args.output}/{args.category}-{helpers.Datetime().now()}.json', 'w') as file:
        file.write(dumps(data, indent=2, ensure_ascii=False))

    helpers.logging.info(f'finish crawling... at {perf_counter() - start}')
    helpers.logging.info(f'data save at {args.output}/{args.category}-{helpers.Datetime().now()}.json')

