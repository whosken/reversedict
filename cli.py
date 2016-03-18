def read_seeds_file(path):
    return open(path).read().split('\n')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Interact with reversedict engine")
    parser.add_argument('description', nargs='?', help='Rough description of intended word.')
    parser.add_argument('-s', '--synonym', nargs='+', help='Synonyms used to filter candidates.')
    parser.add_argument('-i', '--index', action='store_true', help='Index known terms.')
    parser.add_argument('--seeds', nargs='+', help='Terms used to seed term indexing.')
    parser.add_argument('--seeds-file', help='Path to comma-separated seeds')
    parser.add_argument('--max-words', type=int, default=10000, help='Index known terms.')
    parser.add_argument('--reset-dict', action='store_true', default=False, help='Delete existing dictionary.')
    args = parser.parse_args()
    
    import reversedict
    
    if args.index:
        import time
        print 'indexing', args.max_words, 'words'
        time.sleep(1)
        import reversedict.indexer
        seeds = read_seeds_file(args.seeds_file) if args.seeds_file else args.seeds
        reversedict.indexer.index_terms(seeds, args.max_words, args.reset_dict)
        raise SystemExit(1)
    
    if not args.description:
        parser.print_help()
        raise SystemExit(0)
        
    print reversedict.lookup(args.description, args.synonym)
