def file_size(size):
    i = 0
    for u in ['B', 'KB', 'MB', 'GB']:
        if not size >> (i + 10):
            return str((size * 10 >> i) / 10) + u
        i += 10
