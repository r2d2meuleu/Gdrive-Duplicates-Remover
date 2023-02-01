import glob, os, shutil, logging, time
from hashlib import sha256

# Create a custom logger
logger = logging.getLogger('gdrive-duplicate-remover')
logger.propagate = False # do not pass logs to the default logger
logging.basicConfig(
                    level=logging.DEBUG,
                    force=True, # Resets any previous configuration
                    )
# Create handlers
handler = logging.StreamHandler()

# Create formatters and add it to handlers
format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
handler.setFormatter(format)

# Add handlers to the logger
logger.addHandler(handler)
logger.propagate = False
class DuplicateRemover:
    def __init__(self):
        self.HOME_DIRECTORY      = os.getcwd()
        self.FILE_HASHES_UNIQUE  = []
        self.MEMORY_DELETED_BYTE = 0
        self.CHUNK_SIZE          = 65536
        self.DEL_COUNT           = 0
        logger.debug("HOME DIRECTORY : " + str(self.HOME_DIRECTORY))
        logger.debug("DEFAULT BLOCK SIZE : " + str(self.CHUNK_SIZE))


    def calculate_filehash(self, file: str) -> str:
        filehash = sha256()
        try:
            with open(file, 'rb') as f:
                chunk = f.read(self.CHUNK_SIZE)
                while len(chunk) > 0:
                    filehash.update(chunk)
                    chunk = f.read(self.CHUNK_SIZE)
                filehash = filehash.hexdigest()
            return filehash
        except:
            return False

    def check_and_delete_duplicates(self, folder_name) -> None:
        logger.debug("-----------------------Traversing paths in " + folder_name)

        all_dirs_list = [path[0] for path in os.walk(folder_name + '/')]

        logger.debug("-----------------------Traversing Completed!")

        for path in all_dirs_list:
            logger.info("-----------------------Checking directory : " + path)
            os.chdir(path)
            all_dir_current_list = [file for file in os.listdir() if os.path.isfile(file)]
            for file in all_dir_current_list:
                filehash = self.calculate_filehash(file)
                if not filehash in self.FILE_HASHES_UNIQUE:
                    if filehash:
                        self.FILE_HASHES_UNIQUE.append(filehash)
                else:
                    logger.debug("Deleting : " + file)
                    del_file_size = os.path.getsize(file)
                    
                    os.remove(file)
                    self.DEL_COUNT += 1
                    self.MEMORY_DELETED_BYTE += del_file_size
                    
            os.chdir(self.HOME_DIRECTORY)

        

    def main(self, folder_name) -> None:
        logger.info("-----------------------Starting Clean ...")
        self.check_and_delete_duplicates(folder_name)
        logger.info("-----------------------Clean Completed! ...")

        memory_deleted_mb = round(self.MEMORY_DELETED_BYTE / 1048576, 2)

        logger.info('-----------------------Duplicate removal done!')
        logger.debug('-----------------------File cleaned  : ' + str(self.DEL_COUNT))
        logger.debug('-----------------------Total Space saved : ' + str(memory_deleted_mb) + 'MB')


folder_name = input("Enter the folder path : ")
App = DuplicateRemover()
App.main(folder_name)


