#! /usr/bin/env python3


usage = """
This is primefac version 2.0.6.

USAGE:
    primefac [-vs|-sv] [-v|--verbose] [-s|--summary|--summarize] [-t=NUMBER]
             [-r=NUMBER] [-m=[prb][,p-1][,p+1][,ecm][,siqs]] rpn

    The value "rpn" is an expression in reverse Polish notation, also called
    postfix notation, and is evaluated using integer arithmetic.  The values
    that remain on the stack after evaluation are then factored in sequence.

    "-t" specifies the largest prime to use for trial division.  The default
    value for this parameter is 1000.  Using "-t=inf" will make primefac use
    trial division exclusively.

    "-r" is the number of iterations of Pollard's rho algorithm to do before
    calling a cofactor "difficult".  Default == 42,000.  Use "-r=inf" to use
    Pollard's rho algorithm exclusively once trial division is completed.

    If verbosity is invoked, then we provide progress reports and also state
    which algorithms produced which factors during the multifactor phase.

    If the summary and verbosity flags are absent, then the output should be
    identical to the output of the GNU factor command, modulo permutation of
    the factors.  If the verbosity flag is invoked, then we provide progress
    reports, turn on the summary flag, and state which methods yielded which
    factors during the multifactor phase.

    If the summary flag is present, then the output is modified by including
    a single newline between each item's output, before the first, and after
    the last.  Each item's output is also modified by printing a second line
    of data summarizing the results by indicating the number of digits (base
    10) in the input, the number of digits (base 10) in each factor, and the
    factors' multiplicities.  For example:

        >>> user@computer:~$ primefac  -s   24 ! 1 -   7 f
        >>> 
        >>> 620448401733239439359999: 991459181683 625793187653
        >>> Z24  =  P12 x P12  =  625793187653 x 991459181683
        >>> 
        >>> 5040: 2 2 2 2 3 3 5 7
        >>> Z4  =  P1^4 x P1^2 x P1 x P1  =  2^4 x 3^2 x 5 x 7
        >>> 
        >>> user@computer:~$

    Note that primes in the ordinary output lines are listed in the order in
    which they were found, while primes in the summary lines are reported in
    strictly-increasing order.
    
    The single-character versions of the verbosity and summary flags may be
    combined into a single flag, "-vs" or "-sv".

    The "-m" flag controls what methods are used during the difficult-factor
    phase.  The "prb" and "ecm" options can be provided several times to use
    multiple concurrent instances of these methods.  Concurrent applications
    of the p-1, p+1, or SIQS methods confers no benefit over a single usage,
    so repeated listings of those methods are ignored.

    This program can be imported into Python scripts as a module; however, I
    recommend importing them from the module "labmath" instead.  This module
    is available via pip (https://pypi.org/project/labmath/).


INTERNAL DETAILS:
    Factoring:
        We use a three-stage factoring algorithm.
        1.  Trial divide with all primes less than or equal to the specified
            limit.  We trial divide by 2 and 3 regardless of the limit.
        2.  Run Pollard's rho algorithm on whatever remains.  This algorithm
            may split a number into two composite cofactors.  Such cofactors
            remain here until they survive the specified number of rounds of
            the rho algorithm.
        3.  Subject each remaining cofactor to a set of up to five factoring
            methods in parallel:
                Pollard's rho algorithm with Brent's improvement,
                Pollard's p-1 method,
                Williams' p+1 method,
                the elliptic curve method,
                and the self-initializing quadratic sieve.

    RPN:
        The available binary operators are +, -, *, //, %, and **, which all
        indicate the same operations here as they indicate in Python3 source
        code; i.e., they denote addition, subtraction, multiplication, floor
        division, remaindering, and powering.  The available unary operators
        are ! and #, which denote the factorial and primorial, respectively.
        For terminal syntax compatibility reasons, the RPN expression may be
        enclosed in quotes, and five aliases are allowed: x for *, / for //,
        xx for **, f for !, and p for #.


CREDITS:
    Significant parts of this code are derived or outright copied from other
    people's work.  In particular, the SIQS code was derived mostly verbatim
    from https://github.com/skollmann/PyFactorise by Stephan Kollmann, while
    the functions to manipulate points on elliptic curves were copied from a
    reply to the blog post at http://programmingpraxis.com/2010/04/23/.  The
    rest, I believe, is my own work, but I may have forgotten something.

"""

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

