if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser("python cli.py [options] [description]")
    parser.add_option('-p', '--pos', help='Set part-of-speech of targeted word.')
    parser.add_option('-v', '--verbose', action='store_true', help='Print details.')
    (options, args) = parser.parse_args()
    
    if not args:
        parser.print_help()
        raise SystemExit(0)
    
    import reversedict
    print reversedict.lookup(args[0], pos=options.pos,
                             verbose=options.verbose)
    