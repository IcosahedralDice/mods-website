#!/usr/bin/python
import index
import e404
import timeline
import contestants
import search
import static_files
import backward_compatibility

def run():
    print("Creating whole project")
    index.run()
    e404.run()
    timeline.run()
    contestants.run()
    search.run()
    static_files.run()
    backward_compatibility.run()

if __name__ == "__main__":
    run()
