#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ASCII_RANGE 128

/**
 * Advanced pointer techniques demonstration:
 * Different ways to manipulate memory with pointers
 */
void encrypt_version1(char *str, int key) {
    // Method 1: Array indexing (still uses pointers behind the scenes)
    for (int i = 0; str[i] != '\0'; i++) {
        str[i] = (str[i] + key) % ASCII_RANGE;
    }
}

void encrypt_version2(char *str, int key) {
    // Method 2: Explicit pointer arithmetic
    char *ptr = str;
    while (*ptr) {
        *ptr = (*ptr + key) % ASCII_RANGE;
        ptr++;  // Move to next address (ptr = ptr + 1)
    }
}

void encrypt_version3(char *str, int key) {
    // Method 3: Pointer arithmetic in the while condition
    char *ptr = str;
    while (*ptr && (*ptr = (*ptr + key) % ASCII_RANGE) && ptr++);
}

void print_memory_map(const char *str) {
    printf("\n=== MEMORY MAP ===\n");
    printf("String address: %p\n", (void*)str);
    printf("String length: %zu bytes\n", strlen(str));
    printf("\nDetailed memory layout:\n");
    
    const char *ptr = str;
    int offset = 0;
    
    while (*ptr != '\0') {
        printf("  Offset +%d: Address=%p, Value='%c', ASCII=%d, Hex=0x%02X\n",
               offset, (void*)ptr, *ptr, (int)*ptr, (unsigned char)*ptr);
        ptr++;
        offset++;
    }
    
    // Show null terminator
    printf("  Offset +%d: Address=%p, Value='\\0', ASCII=0, Hex=0x00 (NULL TERMINATOR)\n",
           offset, (void*)ptr);
    printf("================\n");
}

int main() {
    char buffer[100];
    char *dynamic_message = NULL;
    int key, choice;
    
    printf("=== ADVANCED POINTER DEMONSTRATION ===\n\n");
    
    // Stack-allocated string (fixed memory)
    printf("1. Stack-allocated string example:\n");
    strcpy(buffer, "Hello World");
    printf("Before encryption: %s\n", buffer);
    printf("Memory address of buffer: %p\n", (void*)buffer);
    encrypt_version2(buffer, 3);
    printf("After encryption: %s\n\n", buffer);
    
    // Heap-allocated string (dynamic memory)
    printf("2. Heap-allocated string example:\n");
    dynamic_message = malloc(100 * sizeof(char));
    if (dynamic_message != NULL) {
        strcpy(dynamic_message, "Dynamic Message");
        printf("Before encryption: %s\n", dynamic_message);
        printf("Memory address (heap): %p\n", (void*)dynamic_message);
        encrypt_version2(dynamic_message, 5);
        printf("After encryption: %s\n", dynamic_message);
        free(dynamic_message);
    }
    
    // Interactive mode with memory mapping
    printf("\n3. Interactive mode with memory mapping:\n");
    printf("Enter a string to encrypt: ");
    fgets(buffer, sizeof(buffer), stdin);
    buffer[strcspn(buffer, "\n")] = '\0';
    
    printf("Enter shift key: ");
    scanf("%d", &key);
    
    print_memory_map(buffer);
    
    printf("\nPerforming encryption...\n");
    encrypt_version2(buffer, key);
    
    print_memory_map(buffer);
    printf("Encrypted result: %s\n", buffer);
    
    return 0;
}