SELECT 
    [database_name] = DB_NAME(database_id),
    [file_name] = f.name,
    [file_type] = f.type_desc,
    [total_latency_ms] = io_stall_read_ms + io_stall_write_ms,
    [read_latency_ms] = io_stall_read_ms,
    [write_latency_ms] = io_stall_write_ms,
    [io_stalls] = io_stall,
    [number_of_reads] = num_of_reads,
    [number_of_writes] = num_of_writes,
    [size_of_file_mb] = size/1204/1000.0,
    [free_space_in_file_mb] = free_space/1204/1000.0
FROM 
    sys.dm_io_virtual_file_stats(NULL, NULL) vfs
INNER JOIN 
    sys.master_files f ON vfs.database_id = f.database_id AND vfs.file_id = f.file_id
WHERE 
    vfs.database_id > 4
ORDER BY 
    io_stall_read_ms + io_stall_write_ms DESC;
