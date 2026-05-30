#include <stdio.h>

int main() {
    double num1, num2;
    char op;

    printf("Enter first number: ");
    scanf("%lf", &num1);

    printf("Enter operator (+, -, *, /): ");
    scanf(" %c", &op);  // space before %c is important!

    printf("Enter second number: ");
    scanf("%lf", &num2);

    if (op == '+') {
        printf("Result = %.2lf\n", num1 + num2);
    }
    else if (op == '-') {
        printf("Result = %.2lf\n", num1 - num2);
    }
    else if (op == '*') {
        printf("Result = %.2lf\n", num1 * num2);
    }
    else if (op == '/') {
        if (num2 == 0) {
            printf("Error: Division by zero is not allowed.\n");
        } else {
            printf("Result = %.2lf\n", num1 / num2);
        }
    }
    else {
        printf("Invalid operator.\n");
    }

    return 0;
}
