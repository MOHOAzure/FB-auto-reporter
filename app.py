def setup():
    """
    return True after setup
    """
    # create blank log and it's folder
    from pathlib import Path
    import os
    log_folder = "log"
    log_name = "log.log"
    log = Path(log_folder,log_name)
    if log.is_file():
        pass
    else:
        os.mkdir(log_folder)
        with open(log, 'x') as fp: 
            pass

    return True
    
if __name__ == "__main__":
    if setup():
        import Scheduler
        Scheduler.run()
    