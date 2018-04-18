import  sys
if __name__ == "__main__":
    minSupport = float(sys.argv[1])
    minconf = float(sys.argv[2])
    frequentfile = sys.argv[3]
    rulefile = sys.argv[4]
    print(minSupport,minconf,frequentfile,rulefile)