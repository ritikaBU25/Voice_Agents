import os
import time

# Set debug mode
os.environ['DEBUG'] = 'true'

def test_silence_logic():
    """Test the silence detection logic directly"""
    print("Testing silence detection logic...")

    # Simulate the silence detection parameters
    silence_threshold = 0.0001
    silence_limit = 10  # 5 seconds / 0.5 second chunks
    silence_count = 0
    prompted = False

    # Simulate 15 chunks of silent audio (RMS = 0.0)
    for i in range(15):
        rms = 0.0  # Truly silent

        print(f"[debug] chunk={i} rms={rms:.6f} silence_count={silence_count} prompted={prompted}")

        if rms > silence_threshold:
            silence_count = 0
            if prompted:
                prompted = False
        else:
            silence_count += 1

        if silence_count >= silence_limit:
            if not prompted:
                print("\n🤔 Are you still there?\n")
                prompted = True
                silence_count = 0
            else:
                print("No response after prompt - ending recording")
                break

        time.sleep(0.1)  # Small delay to simulate real timing

    print("✅ Silence detection test completed")

if __name__ == "__main__":
    test_silence_logic()