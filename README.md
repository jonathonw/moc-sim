MOC-Sim
=======
A simulator for the Untimed, Synchronous, and Timed models of computation, as
described in _Modeling Embedded Systems and SoC's: Concurrency and Time in
Models of Computation_ by Axel Jantsch.

System Requirements
-------------------
This simulator was built using Python 2.6, and should run on any Python version
2.x later than 2.6 (any 2.6 or 2.7 release should work).  Due to breaking API
changes, Python releases 3.0 and later are *not* supported.

Mac OS 10.6 and most recent distributions of Linux should include a compatible
version of Python out of the box (run 'python' from a terminal window); Windows
users can download Python 2.7 from the [Python download page][py-dl].

[py-dl]: http://www.python.org/download/

Getting the simulator
---------------------
You can download the simulator in two ways.  Either:

 *  Download a snapshot of the most recent version of the simulator:
    [Windows (zip)][zip], [Linux/OSX (tar.gz)][tarball]

 *  Or, if you have git installed, clone the repository with:

        git clone git@github.com:jonathonw/moc-sim.git
        
[zip]: https://github.com/jonathonw/moc-sim/zipball/master
[tarball]: https://github.com/jonathonw/moc-sim/tarball/master

Running the simulator
---------------------
The simulator is designed as a command-line utility; it takes in an XML file
specifying the model and its input signals, and outputs the output signals which
were generated after the model has been executed.

On Windows, you can run the simulator from the command prompt with:

    python Simulator.py sample.xml
    
where sample.xml is the XML file containing the model to be simulated.  Also
note that Python must be in the system PATH for the simulator to run; for
more information, see the [Python documentation][python-path].

On Linux or Mac OS X, Python is typically already in the system path.  On such
systems, you should be able to run the simulator with:

    ./Simulator.py sample.xml
    
where sample.xml is the XML file containing the model to be simulated.

[python-path]: http://docs.python.org/using/windows.html#excursus-setting-environment-variables
