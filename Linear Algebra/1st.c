#include <stdio.h>

int main() {
    double a, b, c, d, e, f;
    double D, Dx, Dy, x, y;

    // Input
    printf("Enter values for a, b, c, d, e, f:\n");
    scanf("%lf %lf %lf %lf %lf %lf", &a, &b, &c, &d, &e, &f);

    // Determinants
    D = (a * e) - (b * d);

    if (D == 0) {
        printf("No unique solution exists.\n");
    } else {
        Dx = (c * e) - (b * f);
        Dy = (a * f) - (c * d);

        x = Dx / D;
        y = Dy / D;

        printf("x = %.2lf\n", x);
        printf("y = %.2lf\n", y);
    }

    return 0;
}
