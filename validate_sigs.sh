match=$(python verify_sigs.py)

if [ $match == "False" ]; then
  echo "!! Error: Hashes do not match"
  exit 1
fi

echo "Success: All hashes match"
