#include "CoarsedGrainedLinkedList.h"
#include <iostream>

int main(){
    CoarseGrainedLinkedList list;

    list.add(10);
    list.add(20);
    list.add(30);
    list.display();                  // 10 -> 20 -> 30

    list.remove(20);
    list.display();                  // 10 -> 30

    list.remove(10);
    list.remove(30);
    list.display();                  // list is empty
    std::cout << "size: " << list.getSize() << std::endl;   // 0
    return 0;
}