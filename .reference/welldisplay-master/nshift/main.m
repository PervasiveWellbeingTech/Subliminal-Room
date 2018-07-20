// Program to adjust the color temperature and hue of the screen.

// Copyright 2018 Peter Washington, Pervasive Wellbeing Technology Lab.



#import <Foundation/Foundation.h>
#import "CBBlueLightClient.h"
#import "MacGammaController.h"

#include <mach/mach.h>
#include <mach/mach_time.h>

#define RATE_OF_CHANGE 0.001


static const uint64_t NANOS_PER_USEC = 1000ULL;
static const uint64_t NANOS_PER_MILLISEC = 1000ULL * NANOS_PER_USEC;
static const uint64_t NANOS_PER_SEC = 1000ULL * NANOS_PER_MILLISEC;

static mach_timebase_info_data_t timebase_info;

static uint64_t abs_to_nanos(uint64_t abs) {
    return abs * timebase_info.numer  / timebase_info.denom;
}

static uint64_t nanos_to_abs(uint64_t nanos) {
    return nanos * timebase_info.denom / timebase_info.numer;
}


int main(int argc, const char * argv[]) {
    
    // INITIALIZE VARIABLES
    
    CBBlueLightClient *client = [[CBBlueLightClient alloc] init];
    int time = 0;
    
    // Define wait times.
    uint64_t time_to_wait_subliminal = 100 * NANOS_PER_USEC; // Value of 3 * NANOS_PER_USEC *IS* PERCEIVABLE
    uint64_t time_to_wait_noticeable = 3 * NANOS_PER_SEC;
    
    // DO A TEST RUN:::

    // Set background screen to green.
    [MacGammaController setGammaWithRed:0 green:10 blue:0];
    
    // Wait until resetting settings.
    mach_timebase_info(&timebase_info);
    uint64_t now = mach_absolute_time();
    mach_wait_until(now + time_to_wait_subliminal);
    
    // Restore color settings.
    CGDisplayRestoreColorSyncSettings();
    
    // Wait for short but noticeable time.
    mach_timebase_info(&timebase_info);
    uint64_t now2 = mach_absolute_time();
    mach_wait_until(now2 + time_to_wait_noticeable);
    
    // Set background screen to green.
    [MacGammaController setGammaWithRed:0 green:10 blue:0];
    
    // Wait for short but noticeable time.
    mach_timebase_info(&timebase_info);
    uint64_t now3 = mach_absolute_time();
    mach_wait_until(now3 + time_to_wait_noticeable);
    
    // Restore color settings.
    CGDisplayRestoreColorSyncSettings();
    
    
    
    
    // SUBLIMINAL INTERVENTION STARTS HERE:::
    
    // Wait for 10 seconds.
   // mach_timebase_info(&timebase_info);
    //uint64_t now4 = mach_absolute_time();
    //mach_wait_until(now4 + time_to_wait_noticeable);
    
    unsigned int i;
    for(i = 0; i < 100; i++) {
        // Set background screen to green.
        [MacGammaController setGammaWithRed:0 green:10 blue:0];
        
        // Super quick waiting.
        mach_timebase_info(&timebase_info);
        uint64_t now5 = mach_absolute_time();
        mach_wait_until(now5 + time_to_wait_subliminal);
        
        // Restore color settings.
        CGDisplayRestoreColorSyncSettings();
        
        // Super quick waiting.
        mach_timebase_info(&timebase_info);
        uint64_t now6 = mach_absolute_time();
        mach_wait_until(now6 + time_to_wait_noticeable);
    }
    
    return 0;
}
