import os
import hashlib

def calculate_sha256(file_path):
  """Calculate the SHA-256 checksum of a file."""
  sha256 = hashlib.sha256()
  with open(file_path, 'rb') as file:
      while chunk := file.read(8192):
          sha256.update(chunk)
  return sha256.hexdigest()

def compare_files(directory, file_pattern=".assert", output_file="output.txt"):

  valid_build=True

  """Compare SHA-256 checksums of files with the same name in the given directory."""
  file_checksums = {}

  # Traverse the directory and calculate checksums
  for root, dirs, files in os.walk(directory):
    for file in files:
      if file.endswith(file_pattern):
        file_path = os.path.join(root, file)
        checksum = calculate_sha256(file_path)

        # Append the checksum to the list for the corresponding file name
        file_checksums[file] = file_checksums.get(file, []) + [checksum]

  # Write results to the output file
  with open(output_file, 'w') as output:
    # Check if there are any files with mismatched checksums
    for file, checksums in file_checksums.items():
      if len(checksums) > 1:
        if len(set(checksums)) > 1:
          output.write(f"File '{file}' has mismatched SHA-256 checksums: {checksums} \n")
          valid_build=False
        else:
          output.write(f"File '{file}' has matching SHA-256 checksums. \n")
      else:
        output.write(f"File '{file}' not enough validators \n")
        valid_build=False

    return valid_build

if __name__ == "__main__":
  directory_to_check = "."
  valid_build = compare_files(directory_to_check)
  print(valid_build)
