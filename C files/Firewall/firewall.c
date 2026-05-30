#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_PACKETS 10
#define MAX_LINE_LENGTH 100

typedef struct {
    int serial_no;
    int priority;
} Packet;

// Comparison function for qsort
int compare_packets(const void *a, const void *b) {
    Packet *p1 = (Packet *)a;
    Packet *p2 = (Packet *)b;
    
    // First compare by priority (lower number = higher priority)
    if (p1->priority != p2->priority) {
        return p1->priority - p2->priority;
    }
    // If priorities are equal, compare by serial number (lower first)
    return p1->serial_no - p2->serial_no;
}

int read_packets_from_file(const char *filename, Packet packets[], int *count) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error: Could not open file '%s'\n", filename);
        return 0;
    }
    
    char line[MAX_LINE_LENGTH];
    *count = 0;
    
    while (fgets(line, sizeof(line), file) && *count < MAX_PACKETS) {
        // Remove newline character
        line[strcspn(line, "\n")] = 0;
        
        // Skip empty lines
        if (strlen(line) == 0) {
            continue;
        }
        
        // Parse serial number and priority
        if (sscanf(line, "%d,%d", &packets[*count].serial_no, &packets[*count].priority) == 2) {
            (*count)++;
        } else {
            printf("Warning: Skipping invalid line: %s\n", line);
        }
    }
    
    fclose(file);
    return 1;
}

void display_packets(Packet packets[], int count) {
    printf("\nSorted Serial Numbers (by priority, then serial):\n");
    printf("----------------------------------------\n");
    for (int i = 0; i < count; i++) {
        printf("Serial: %d, Priority: %d\n", packets[i].serial_no, packets[i].priority);
    }
}

int main(int argc, char *argv[]) {
    Packet packets[MAX_PACKETS];
    int packet_count = 0;
    char filename[256];
    
    // Get filename from command line argument or use default
    if (argc > 1) {
        strcpy(filename, argv[1]);
    } else {
        strcpy(filename, "packets.txt");
        printf("No input file specified. Using default: %s\n", filename);
    }
    
    // Read packets from file
    if (!read_packets_from_file(filename, packets, &packet_count)) {
        return 1;
    }
    
    if (packet_count == 0) {
        printf("No valid packets found in file.\n");
        return 1;
    }
    
    printf("Read %d packet(s) from file.\n", packet_count);
    
    // Sort packets
    qsort(packets, packet_count, sizeof(Packet), compare_packets);
    
    // Display results
    display_packets(packets, packet_count);
    
    return 0;
}