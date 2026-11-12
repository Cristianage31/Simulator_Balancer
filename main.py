from engine.simulation import TycoonSimulation

if __name__ == "__main__":
    print("Initializing Headless Tycoon Simulation (Phase 1)...")
    
    sim = TycoonSimulation(dt=0.05)
    results = sim.run_to_completion(max_time=120.0) # change to 120 or 1200
    
    print(f"Simulation finished. Total ticks recorded: {len(results)}")
    print("Sample telemetry (first 5 ticks):")
    for r in results[:5]:
        print(r)
        
    print("\nSample telemetry (last 5 ticks):")
    for r in results[-5:]:
        print(r)