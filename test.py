from subprocess import run
import os
sunny2 = '/home/marco/Documents/uni/tesi/sunny-cp2/bin/sunny-cp'
sunny = '/home/marco/Documents/uni/tesi/sunny-cp/bin/sunny-cp'
mzns = [f'/home/marco/Documents/uni/tesi/sunny-cp/test/examples/{file}' for file in os.listdir("test/examples")]
skip = ["/home/marco/Documents/uni/tesi/sunny-cp/test/examples/battleships_1.mzn",
        "/home/marco/Documents/uni/tesi/sunny-cp/test/examples/alpha.mzn"]
for test in mzns:
    if test in skip:
        continue
    sun1 = run(["python3", sunny, test], capture_output=True)
    sun2 = run(["python2", sunny2, test], capture_output=True)
    print(test)
    for s1, s2 in zip(sorted(sun1.stdout.decode("utf8").split("\n")), sorted(sun2.stdout.decode("utf8").split("\n"))):
        if s1 != s2 and not (("% Search completed at time: " in s1 and "% Search completed at time: " in s2) or
        ("% Search completed at time: " in s1 and "% Search completed at time: " in s2) or
        ("% Current Solution Time: " in s1 and "% Current Solution Time: " in s2)):
            print("\t", s1)
            print("\t", s2)