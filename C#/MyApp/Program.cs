using System;

class Program
{
    static float[] Input()
    {
        float[] numArr = new float[2];

        Console.WriteLine("Enter your First Number:");
        numArr[0] = float.Parse(Console.ReadLine());

        Console.WriteLine("Enter your Second Number:");
        numArr[1] = float.Parse(Console.ReadLine());

        return numArr;
    }

    static float add(float a, float b) => a + b;

    static float sub(float a, float b) => a - b;

    static float product(float a, float b) => a * b;

    static float divide(float a, float b)
    {
        if (b == 0)
        {
            Console.WriteLine("Cannot divide by zero!");
            return 0;
        }

        return a / b;
    }

    static void menu()
    {
        Console.WriteLine("\nWelcome to C# Calculator!");
        Console.WriteLine("1. Addition");
        Console.WriteLine("2. Subtraction");
        Console.WriteLine("3. Product");
        Console.WriteLine("4. Division");
    }

    static float calc()
    {
        menu();

        Console.WriteLine("Enter choice:");
        int key = int.Parse(Console.ReadLine());

        float[] numArr = Input();
        float total = 0;

        if (key == 1)
        {
            total = add(numArr[0], numArr[1]);
        }
        else if (key == 2)
        {
            total = sub(numArr[0], numArr[1]);
        }
        else if (key == 3)
        {
            total = product(numArr[0], numArr[1]);
        }
        else if (key == 4)
        {
            total = divide(numArr[0], numArr[1]);
        }
        else
        {
            Console.WriteLine("Invalid Choice");
        }

        return total;
    }

    static void Main()
    {
        Console.WriteLine("Result = " + calc());
    }
}