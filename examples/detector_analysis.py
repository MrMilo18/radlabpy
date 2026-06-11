"""
Basic detector analysis example using radlabpy.

This example demonstrates how to calculate:

- detection efficiency;
- binomial efficiency uncertainty;
- event rate;
- Poisson rate uncertainty;
- coincidence rate;
- accidental coincidence rate;
- signal-to-noise ratio.

The numerical values are simple and physically interpretable.
"""

from radlabpy.detectors import (
    accidental_coincidence_rate,
    coincidence_rate,
    detection_efficiency,
    efficiency_uncertainty,
    event_rate,
    rate_uncertainty,
    signal_to_noise,
)


def main():
    """Run a simple detector analysis example."""

    # Suppose a source emits or generates 1000 particles/events.
    # The detector records 850 of them.
    emitted_events = 1000
    detected_events = 850

    efficiency = detection_efficiency(detected_events, emitted_events)
    sigma_efficiency = efficiency_uncertainty(detected_events, emitted_events)

    # Suppose the detector measured 1200 events in 60 seconds.
    counts = 1200
    measurement_time = 60.0  # seconds

    rate = event_rate(counts, measurement_time)
    sigma_rate = rate_uncertainty(counts, measurement_time)

    # Suppose a two-channel system measured 180 coincidences in 60 seconds.
    coincidences = 180
    coincidence_measurement_time = 60.0  # seconds

    coincidence = coincidence_rate(coincidences, coincidence_measurement_time)

    # Suppose the two individual detector rates are 25 Hz and 30 Hz.
    # The coincidence window is 100 ns = 100e-9 s.
    rate_channel_1 = 25.0  # Hz
    rate_channel_2 = 30.0  # Hz
    coincidence_window = 100e-9  # seconds

    accidental = accidental_coincidence_rate(
        rate_channel_1,
        rate_channel_2,
        coincidence_window,
    )

    # Suppose the signal amplitude is 50 units and the noise is 5 units.
    signal = 50.0
    noise = 5.0

    snr = signal_to_noise(signal, noise)

    print("Basic detector analysis")
    print("=======================")
    print(f"Emitted events: {emitted_events}")
    print(f"Detected events: {detected_events}")
    print(f"Detection efficiency: {efficiency:.4f}")
    print(f"Efficiency uncertainty: {sigma_efficiency:.4f}")
    print()
    print(f"Counts: {counts}")
    print(f"Measurement time: {measurement_time:.1f} s")
    print(f"Event rate: {rate:.4f} counts/s")
    print(f"Rate uncertainty: {sigma_rate:.4f} counts/s")
    print()
    print(f"Coincidences: {coincidences}")
    print(f"Coincidence rate: {coincidence:.4f} coincidences/s")
    print()
    print(f"Channel 1 rate: {rate_channel_1:.4f} Hz")
    print(f"Channel 2 rate: {rate_channel_2:.4f} Hz")
    print(f"Coincidence window: {coincidence_window:.2e} s")
    print(f"Accidental coincidence rate: {accidental:.6e} Hz")
    print()
    print(f"Signal: {signal:.4f}")
    print(f"Noise: {noise:.4f}")
    print(f"Signal-to-noise ratio: {snr:.4f}")


if __name__ == "__main__":
    main()