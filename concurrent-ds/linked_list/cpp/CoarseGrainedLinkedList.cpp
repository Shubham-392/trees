#include "CoarsedGrainedLinkedList.h"
#include <vector>
#include <mutex>

// constructor and destructor overriding
// no need ot overide destructor as cpp automatically calls parent class destructor
// in the program
// vector initialization of linked list 
CoarseGrainedLinkedList::CoarseGrainedLinkedList(const std::vector<int>& arr): UnSyncLinkedList(arr){}

void CoarseGrainedLinkedList::add(int key){
    std::lock_guard<std::mutex> lock(mux_);
    UnSyncLinkedList::m_add(key);
}

void CoarseGrainedLinkedList::remove(int key){
    std::lock_guard<std::mutex> lock(mux_);
    UnSyncLinkedList::m_remove(key);
}

int CoarseGrainedLinkedList::getSize(){
    std::lock_guard<std::mutex> lock(mux_);
    int size =  UnSyncLinkedList::m_getSize();
    return size;
}

LinkedListNode* CoarseGrainedLinkedList::getHead(){
    std::lock_guard<std::mutex> lock(mux_);
    // m_head from parent class
    return m_head;
}
LinkedListNode* CoarseGrainedLinkedList::getTail(){
    std::lock_guard<std::mutex> lock(mux_);
    // m_head from parent class
    return m_tail;
}

void CoarseGrainedLinkedList::display(){
    std::lock_guard<std::mutex> lock(mux_);
    UnSyncLinkedList::m_display();
}