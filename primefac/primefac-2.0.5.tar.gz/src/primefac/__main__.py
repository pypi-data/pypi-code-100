#! /usr/bin/env python3

if __name__ == "__main__":
    from sys import exit, argv
    if len(argv) == 1: exit(usage)
    if any("h" in arg for arg in argv) or any("?" in arg for arg in argv): exit(usage)
    start, rpx, tr, rr, verbose, summarize = 1, [], 1000, 42000, False, False
    ms = {"prb":pollardrho_brent, "p-1":pollard_pm1, "p+1":williams_pp1, "ecm":ecm, "siqs":siqs}
    methods = (pollardrho_brent, pollard_pm1, williams_pp1, ecm, siqs)
    try:
        for arg in argv[1:]:
            if arg in ("-v", "--verbose"): verbose, summarize = True, True
            elif arg in ("-s", "--summary", "--summarize"): summarize = True
            elif arg in ("-vs", "-sv"): verbose, summarize = True, True
            elif arg[:3] == "-t=": tr = inf if arg[3:] == "inf" else int(arg[3:])    # Maximum number for trial division
            elif arg[:3] == "-r=": rr = inf if arg[3:] == "inf" else int(arg[3:])    # Number of rho rounds before multifactor
            elif arg[:3] == "-m=": #methods = tuple(ms[x] for x in arg[3:].split(',') if x in ms)
                methods = []
                for x in arg[3:].split(','):
                    if x in ms:
                        if x in ("p-1", "p+1", "siqs") and ms[x] in methods: continue
                        methods.append(ms[x])
            else: rpx.append(arg)
        nums = rpn(' '.join(rpx))
    except: exit("Error while parsing arguments.  To view usage, invoke with -h, --help, or -?.")
    if summarize: print()
    for n in nums:
        assert isinstance(n, int)
        print("%d:" % n, end='', flush=True)
        f = {}
        flist = []
        for p in primefac(n, trial=(n if tr == "inf" else tr), rho=rr, verbose=verbose, methods=methods):
            f[p] = f.get(p, 0) + 1
            flist.append(p)
            if not verbose: print(" %d" % p, end='', flush=True)
            assert isprime(p) and n%p == 0, (n, p)
        if verbose:
            print()
            print("%d:" % n, end='')
            for p in flist: print(" %d" % p, end='')
        print()
        if summarize:
            print("Z%d  = " % len(str(n)), end=' ')
            outstr = ""
            for p in sorted(f):
                if f[p] == 1: outstr += "P%d x " % len(str(p))
                else: outstr += "P%d^%d x " % (len(str(p)), f[p])
            outstr = outstr[:-2] + " = "
            for p in sorted(f):
                if f[p] == 1: outstr += " %d x" % p
                else: outstr += " %d^%d x" % (p, f[p])
            print(outstr[:-2])
            print()
    exit()

# testdata = [factorial(24) - 1, factorial(38) + 1, factorial(40) - 1, factorial(44) + 1, factorial(54) + 1]

