def na(score = None):
    if score:
        return 'NA score is %s' % score
    else:
        return 'failed.'

if __name__ == '__main__':
    import sys
    print sys.argv
    if len(sys.argv) >= 2:
        print na(sys.argv[1])
    else:
        print na()
