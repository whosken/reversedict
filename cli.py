if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Interact with reversedict engine")
    parser.add_argument('description', nargs='?', help='Rough description of intended word.')
    parser.add_argument('-s', '--synonym', nargs='+', help='Synonyms used to filter candidates.')
    parser.add_argument('-i', '--index', action='store_true', help='Index known terms.')
    args = parser.parse_args()
    
    import reversedict
    
    if args.index:
        import reversedict.indexer
        reversedict.indexer.index_terms()
        raise SystemExit(1)
    
    if not args.description:
        parser.print_help()
        raise SystemExit(0)
        
    print reversedict.lookup(args.description, args.synonym)
    