#include "UnSyncLinkedList.h"
#include <vector>


UnSyncLinkedList::UnSyncLinkedList(const std::vector<int>& arr){
    // we have to insert the element from arr
    for (const auto& key: arr){
        m_add(key);
    }
}


void UnSyncLinkedList::m_add(int key){
    LinkedListNode* new_node = new LinkedListNode(key);
    if (m_head == nullptr){
        m_head = new_node;
        m_tail = new_node;
    } else {
        m_tail->next = new_node;
        m_tail = new_node;
    }
    // increase the size gloally
    m_size++;
}


bool UnSyncLinkedList::m_remove(int key){
   
}
