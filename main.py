import sys

if __name__ == '__main__':
    # Run tests
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        from engine.logic import core_tests
        core_tests.run()
        
    # Run profiler
    elif len(sys.argv) > 1 and sys.argv[1] == 'profile':
        from engine.profile_lib import profiler
        profiler.run("")
    
    # View profiling results
    elif len(sys.argv) > 1 and sys.argv[1] == 'view':
        from engine.profile_lib import profiler
        profiler.view("")
        
    # Run the game
    else:
        from game import downstream
        d = downstream.Downstream()
        d.start()
