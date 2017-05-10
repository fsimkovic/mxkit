
__author__ = "Felix Simkovic"
__date__ = "09 May 2017"
__version__ = "0.1"

import os
import time

import mbkit.dispatch.cluster
import mbkit.dispatch.local


def submit_job(script, qtype, *args, **kwargs):
    """SOME FANCY TEXT
    
    Parameters
    ----------
    script : list
       A list of one or more scripts with absolute paths
    qtype : str
       The queue type to submit the jobs to [ local | sge ]

    Returns
    -------
    bool
       The final status about the job execution

    Raises
    ------
    ValueError
       One or more scripts cannot be found
    ValueError
       One or more scripts are not executable
    ValueError
       Unknown queue type provided

    """
    if not('directory' in kwargs and kwargs['directory']):
        kwargs['directory'] = os.getcwd()

    # Quick check if all scripts are sound
    if not all(os.path.isfile(fpath) for fpath in script):
        raise ValueError("One or more scripts cannot be found")
    elif not all(os.access(fpath, os.X_OK) for fpath in script):
        raise ValueError("One or more scripts are not executable")
    # Submit the job to the corresponding queue
    array_job_on_order = True if len(script) > 1 else True
    if qtype == "local":
        mbkit.dispatch.local.LocalJobServer.sub(script, **kwargs)
    elif qtype == "sge":
        # Array job - deal with it
        if array_job_on_order:
            array = (1, len(script), len(script))
            # Write all jobs into an array.jobs file
            array_jobs = os.path.join(kwargs['directory'], 'array.jobs')
            with open(array_jobs, 'w') as f_out:
                f_out.write(os.linesep.join(script))
            # Create a array.scripts file used to execute the array
            array_script = os.path.join(kwargs['directory'], "array.script")
            with open(array_script, 'w') as f_out:
                f_out.write(os.linesep.join([
                    "#!/bin/sh", 
                    "script=`sed -n \"${{SGE_TASK_ID}}p\" {0}`".format(array_jobs),
                    "$script",
                ]))
            kwargs['log'] = "arrayJob_$TASK_ID.log"
            script = [array_script]
        # Submit the jobs
        qobj = mbkit.dispatch.cluster.SunGridEngine
        pid = qobj.qsub(script, array=array, **kwargs)
        while qobj.qstat(pid):
            time.sleep(60)
        # Finally, we need to rename arrayJob_X.log files
        if array_job_on_order:
            qobj.rename_array_logs(array_jobs, kwargs['directory'])
    else:
        raise ValueError("Unknown queue: {0}".format(queue))
    
    return True
