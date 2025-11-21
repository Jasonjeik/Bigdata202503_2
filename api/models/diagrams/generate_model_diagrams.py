"""
Generador de diagramas de arquitectura de modelos para presentación
Basado en el notebook Modelos_ML.ipynb
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

# Configuración general
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

def create_logistic_regression_diagram():
    """Modelo 1: Logistic Regression + TF-IDF"""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Título
    ax.text(5, 5.5, 'Modelo 1: Logistic Regression + TF-IDF', 
            ha='center', fontsize=16, fontweight='bold')
    
    # Input
    input_box = FancyBboxPatch((0.5, 2), 1.5, 1.5, boxstyle="round,pad=0.1", 
                               edgecolor='#2E86AB', facecolor='#A9D6E5', linewidth=2)
    ax.add_patch(input_box)
    ax.text(1.25, 2.75, 'Input Text\n(Review)', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # TF-IDF Vectorizer
    tfidf_box = FancyBboxPatch((2.5, 1.8), 2, 2, boxstyle="round,pad=0.1",
                               edgecolor='#E63946', facecolor='#F1FAEE', linewidth=2)
    ax.add_patch(tfidf_box)
    ax.text(3.5, 3.3, 'TF-IDF Vectorizer', ha='center', fontsize=11, fontweight='bold')
    ax.text(3.5, 2.8, 'max_features: 10K-20K', ha='center', fontsize=8)
    ax.text(3.5, 2.5, 'ngram_range: (1,1)-(1,2)', ha='center', fontsize=8)
    ax.text(3.5, 2.2, 'stop_words: english', ha='center', fontsize=8)
    
    # Logistic Regression
    lr_box = FancyBboxPatch((5.5, 2), 1.8, 1.5, boxstyle="round,pad=0.1",
                            edgecolor='#457B9D', facecolor='#A8DADC', linewidth=2)
    ax.add_patch(lr_box)
    ax.text(6.4, 3.1, 'Logistic\nRegression', ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(6.4, 2.4, 'C: 0.1-10', ha='center', fontsize=8)
    
    # Output
    output_box = FancyBboxPatch((8, 2.2), 1.5, 1, boxstyle="round,pad=0.1",
                                edgecolor='#06A77D', facecolor='#90EE90', linewidth=2)
    ax.add_patch(output_box)
    ax.text(8.75, 2.7, 'Sentiment\n(0 or 1)', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Arrows
    arrow1 = FancyArrowPatch((2, 2.75), (2.5, 2.75), arrowstyle='->', lw=2, color='black')
    arrow2 = FancyArrowPatch((4.5, 2.75), (5.5, 2.75), arrowstyle='->', lw=2, color='black')
    arrow3 = FancyArrowPatch((7.3, 2.75), (8, 2.75), arrowstyle='->', lw=2, color='black')
    ax.add_patch(arrow1)
    ax.add_patch(arrow2)
    ax.add_patch(arrow3)
    
    # GridSearchCV annotation
    grid_box = FancyBboxPatch((2.5, 0.3), 4.8, 0.8, boxstyle="round,pad=0.05",
                              edgecolor='#F77F00', facecolor='#FCBF49', linewidth=1.5, linestyle='--')
    ax.add_patch(grid_box)
    ax.text(4.9, 0.7, 'GridSearchCV (3-fold CV) - Hyperparameter Tuning', 
            ha='center', fontsize=9, fontweight='bold', style='italic')
    
    # Accuracy
    ax.text(5, 1.2, f'Best Validation Accuracy: ~88.40%', 
            ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('api/models/diagrams/model1_logistic_regression.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Diagrama 1 generado: model1_logistic_regression.png")
    plt.close()

def create_random_forest_diagram():
    """Modelo 2: Random Forest"""
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    
    # Título
    ax.text(5, 6.5, 'Modelo 2: Random Forest + TF-IDF', 
            ha='center', fontsize=16, fontweight='bold')
    
    # Input
    input_box = FancyBboxPatch((0.5, 2.5), 1.5, 1.5, boxstyle="round,pad=0.1",
                               edgecolor='#2E86AB', facecolor='#A9D6E5', linewidth=2)
    ax.add_patch(input_box)
    ax.text(1.25, 3.25, 'Input Text\n(Review)', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # TF-IDF
    tfidf_box = FancyBboxPatch((2.5, 2.3), 1.8, 2, boxstyle="round,pad=0.1",
                               edgecolor='#E63946', facecolor='#F1FAEE', linewidth=2)
    ax.add_patch(tfidf_box)
    ax.text(3.4, 3.8, 'TF-IDF', ha='center', fontsize=11, fontweight='bold')
    ax.text(3.4, 3.4, 'max_features:', ha='center', fontsize=8)
    ax.text(3.4, 3.1, '20,000', ha='center', fontsize=8, fontweight='bold')
    ax.text(3.4, 2.7, 'ngram: (1,2)', ha='center', fontsize=8)
    
    # Random Forest (ensemble de árboles)
    rf_y_start = 2
    tree_positions = [5.2, 5.8, 6.4]
    
    for i, x_pos in enumerate(tree_positions):
        tree = FancyBboxPatch((x_pos - 0.25, rf_y_start), 0.5, 2.5, boxstyle="round,pad=0.05",
                              edgecolor='#2D6A4F', facecolor='#95D5B2', linewidth=1.5)
        ax.add_patch(tree)
        
        # Dibujar estructura de árbol simplificada
        for level in range(3):
            y = rf_y_start + 2.2 - level * 0.6
            circle = Circle((x_pos, y), 0.08, color='#1B4332')
            ax.add_patch(circle)
            if level < 2:
                ax.plot([x_pos, x_pos - 0.12], [y, y - 0.6], 'k-', lw=0.8)
                ax.plot([x_pos, x_pos + 0.12], [y, y - 0.6], 'k-', lw=0.8)
        
        ax.text(x_pos, rf_y_start + 0.3, f'Tree {i+1}', ha='center', fontsize=7, fontweight='bold')
    
    # Label "Random Forest"
    ax.text(5.8, 4.8, 'Random Forest Ensemble', ha='center', fontsize=11, fontweight='bold')
    ax.text(5.8, 5.3, 'n_estimators: 100-200', ha='center', fontsize=8)
    ax.text(5.8, 5.6, 'max_depth: 20 or None', ha='center', fontsize=8)
    
    # Voting
    voting_box = FancyBboxPatch((7.2, 2.5), 1, 1.5, boxstyle="round,pad=0.1",
                                edgecolor='#6A4C93', facecolor='#C9ADA7', linewidth=2)
    ax.add_patch(voting_box)
    ax.text(7.7, 3.25, 'Majority\nVoting', ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Output
    output_box = FancyBboxPatch((8.5, 2.7), 1.2, 1, boxstyle="round,pad=0.1",
                                edgecolor='#06A77D', facecolor='#90EE90', linewidth=2)
    ax.add_patch(output_box)
    ax.text(9.1, 3.2, 'Sentiment\n(0 or 1)', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Arrows
    arrow1 = FancyArrowPatch((2, 3.25), (2.5, 3.25), arrowstyle='->', lw=2, color='black')
    arrow2 = FancyArrowPatch((4.3, 3.25), (4.95, 3.25), arrowstyle='->', lw=2, color='black')
    
    for tree_x in tree_positions:
        arrow_tree = FancyArrowPatch((tree_x, 3.25), (7.2, 3.25), arrowstyle='->', lw=1.5, color='gray', alpha=0.6)
        ax.add_patch(arrow_tree)
    
    arrow4 = FancyArrowPatch((8.2, 3.2), (8.5, 3.2), arrowstyle='->', lw=2, color='black')
    ax.add_patch(arrow1)
    ax.add_patch(arrow2)
    ax.add_patch(arrow4)
    
    # GridSearchCV
    grid_box = FancyBboxPatch((4.8, 0.5), 3.5, 0.8, boxstyle="round,pad=0.05",
                              edgecolor='#F77F00', facecolor='#FCBF49', linewidth=1.5, linestyle='--')
    ax.add_patch(grid_box)
    ax.text(6.55, 0.9, 'GridSearchCV (3-fold CV)', ha='center', fontsize=9, fontweight='bold', style='italic')
    
    # Accuracy
    ax.text(5, 1.5, f'Best Validation Accuracy: ~85.12%', 
            ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('api/models/diagrams/model2_random_forest.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Diagrama 2 generado: model2_random_forest.png")
    plt.close()

def create_lstm_diagram():
    """Modelo 3: LSTM con Optuna"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Título
    ax.text(7, 7.5, 'Modelo 3: LSTM Neural Network (Optuna Optimized)', 
            ha='center', fontsize=16, fontweight='bold')
    
    # Input
    input_box = FancyBboxPatch((0.5, 3), 1.5, 1.5, boxstyle="round,pad=0.1",
                               edgecolor='#2E86AB', facecolor='#A9D6E5', linewidth=2)
    ax.add_patch(input_box)
    ax.text(1.25, 3.75, 'Input Text\n(Review)', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Embedding
    emb_box = FancyBboxPatch((2.5, 2.8), 1.8, 2, boxstyle="round,pad=0.1",
                             edgecolor='#E63946', facecolor='#FFE5E5', linewidth=2)
    ax.add_patch(emb_box)
    ax.text(3.4, 4.3, 'Embedding\nLayer', ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(3.4, 3.5, 'vocab_size: 30,002', ha='center', fontsize=8)
    ax.text(3.4, 3.2, 'embed_dim: 224', ha='center', fontsize=8, fontweight='bold', color='#E63946')
    
    # LSTM Layers
    lstm_box = FancyBboxPatch((5, 2.3), 3, 3, boxstyle="round,pad=0.1",
                              edgecolor='#457B9D', facecolor='#CAF0F8', linewidth=2)
    ax.add_patch(lstm_box)
    ax.text(6.5, 4.8, 'Bidirectional LSTM', ha='center', fontsize=12, fontweight='bold')
    
    # LSTM cells visualization
    for layer in range(2):
        y_base = 4.0 - layer * 1.2
        for direction, x_offset in [('→', 0), ('←', 0.6)]:
            cell_box = FancyBboxPatch((5.3 + x_offset, y_base - 0.3), 0.5, 0.6,
                                      boxstyle="round,pad=0.02", edgecolor='#023E8A',
                                      facecolor='#0077B6', linewidth=1)
            ax.add_patch(cell_box)
            ax.text(5.55 + x_offset, y_base, direction, ha='center', va='center',
                    fontsize=14, color='white', fontweight='bold')
        
        ax.text(7.3, y_base, f'Layer {layer + 1}', ha='left', fontsize=9)
    
    ax.text(6.5, 3.0, 'hidden_dim: 192', ha='center', fontsize=8, fontweight='bold', color='#023E8A')
    ax.text(6.5, 2.7, 'num_layers: 2', ha='center', fontsize=8)
    ax.text(6.5, 2.4, 'dropout: 0.3-0.6', ha='center', fontsize=8)
    
    # Fully Connected Layers
    fc_layers = [
        ('FC1', 8.5, 128, '#2D6A4F'),
        ('FC2', 9.8, 64, '#40916C'),
        ('Output', 11.1, 2, '#52B788')
    ]
    
    for name, x_pos, units, color in fc_layers:
        fc_box = FancyBboxPatch((x_pos, 2.8), 0.8, 2, boxstyle="round,pad=0.1",
                                edgecolor=color, facecolor=f'{color}40', linewidth=2)
        ax.add_patch(fc_box)
        ax.text(x_pos + 0.4, 4.3, name, ha='center', fontsize=10, fontweight='bold')
        ax.text(x_pos + 0.4, 3.8, f'{units} units', ha='center', fontsize=8)
        
        # Dropout annotation
        if name != 'Output':
            ax.text(x_pos + 0.4, 3.3, 'Dropout', ha='center', fontsize=7, style='italic', color='red')
    
    # Final Output
    output_box = FancyBboxPatch((12.2, 3.2), 1.3, 1, boxstyle="round,pad=0.1",
                                edgecolor='#06A77D', facecolor='#90EE90', linewidth=2)
    ax.add_patch(output_box)
    ax.text(12.85, 3.7, 'Sentiment\n(0 or 1)', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Arrows
    arrows = [
        ((2, 3.75), (2.5, 3.75)),
        ((4.3, 3.75), (5, 3.75)),
        ((8, 3.75), (8.5, 3.75)),
        ((9.3, 3.75), (9.8, 3.75)),
        ((10.6, 3.75), (11.1, 3.75)),
        ((11.9, 3.7), (12.2, 3.7))
    ]
    
    for start, end in arrows:
        arrow = FancyArrowPatch(start, end, arrowstyle='->', lw=2, color='black')
        ax.add_patch(arrow)
    
    # Optuna annotation
    optuna_box = FancyBboxPatch((1, 1), 12, 0.8, boxstyle="round,pad=0.05",
                                edgecolor='#9D4EDD', facecolor='#E0AAFF', linewidth=2, linestyle='--')
    ax.add_patch(optuna_box)
    ax.text(7, 1.4, 'Optuna Hyperparameter Optimization (10 trials) + 5-Fold Cross-Validation', 
            ha='center', fontsize=10, fontweight='bold', style='italic')
    
    # Accuracy
    ax.text(7, 0.4, f'CV Mean Accuracy: ~87.38% | Best Fold: 88.12%', 
            ha='center', fontsize=11, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5), fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('api/models/diagrams/model3_lstm.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Diagrama 3 generado: model3_lstm.png")
    plt.close()

def create_distilbert_diagram():
    """Modelo 4: DistilBERT"""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    # Título
    ax.text(7, 8.5, 'Modelo 4: DistilBERT (Transformer Architecture)', 
            ha='center', fontsize=16, fontweight='bold')
    
    # Input
    input_box = FancyBboxPatch((0.5, 3.5), 1.5, 1.5, boxstyle="round,pad=0.1",
                               edgecolor='#2E86AB', facecolor='#A9D6E5', linewidth=2)
    ax.add_patch(input_box)
    ax.text(1.25, 4.25, 'Input Text\n(Review)', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Tokenizer
    tok_box = FancyBboxPatch((2.5, 3.3), 1.8, 2, boxstyle="round,pad=0.1",
                             edgecolor='#E63946', facecolor='#FFE5E5', linewidth=2)
    ax.add_patch(tok_box)
    ax.text(3.4, 4.8, 'WordPiece\nTokenizer', ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(3.4, 3.9, 'max_length: 256', ha='center', fontsize=8)
    ax.text(3.4, 3.6, 'vocab: 30,522', ha='center', fontsize=8)
    
    # DistilBERT Transformer Blocks
    transformer_box = FancyBboxPatch((5, 2), 6, 5, boxstyle="round,pad=0.15",
                                     edgecolor='#5A189A', facecolor='#E0C3FC', linewidth=3)
    ax.add_patch(transformer_box)
    ax.text(8, 6.6, 'DistilBERT Transformer (6 Layers)', ha='center', fontsize=12, fontweight='bold')
    
    # Transformer layers
    for i in range(3):
        y_start = 5.5 - i * 1.3
        
        # Multi-Head Attention
        attn_box = FancyBboxPatch((5.5, y_start), 2.2, 0.8, boxstyle="round,pad=0.05",
                                  edgecolor='#7209B7', facecolor='#C77DFF', linewidth=1.5)
        ax.add_patch(attn_box)
        ax.text(6.6, y_start + 0.4, 'Multi-Head\nAttention', ha='center', va='center',
                fontsize=8, fontweight='bold')
        
        # Feed Forward
        ff_box = FancyBboxPatch((8.2, y_start), 2.2, 0.8, boxstyle="round,pad=0.05",
                                edgecolor='#9D4EDD', facecolor='#E0AAFF', linewidth=1.5)
        ax.add_patch(ff_box)
        ax.text(9.3, y_start + 0.4, 'Feed\nForward', ha='center', va='center',
                fontsize=8, fontweight='bold')
        
        # Arrows between components
        ax.annotate('', xy=(8.2, y_start + 0.4), xytext=(7.7, y_start + 0.4),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
        
        if i < 2:
            ax.annotate('', xy=(8, y_start - 0.4), xytext=(8, y_start),
                       arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
    
    ax.text(8, 2.5, '6 Transformer Layers', ha='center', fontsize=9, style='italic')
    ax.text(8, 2.2, '66M Parameters', ha='center', fontsize=8, fontweight='bold', color='#5A189A')
    
    # Classification Head
    class_box = FancyBboxPatch((11.5, 3.5), 1.5, 1.5, boxstyle="round,pad=0.1",
                               edgecolor='#2D6A4F', facecolor='#95D5B2', linewidth=2)
    ax.add_patch(class_box)
    ax.text(12.25, 4.5, 'Classification\nHead', ha='center', va='center',
            fontsize=10, fontweight='bold')
    ax.text(12.25, 3.8, '2 classes', ha='center', fontsize=8)
    
    # Final Output
    output_box = FancyBboxPatch((13, 3.7), 0.8, 1, boxstyle="round,pad=0.1",
                                edgecolor='#06A77D', facecolor='#90EE90', linewidth=2)
    ax.add_patch(output_box)
    ax.text(13.4, 4.2, 'Sentiment', ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Main flow arrows
    main_arrows = [
        ((2, 4.25), (2.5, 4.25)),
        ((4.3, 4.25), (5, 4.25)),
        ((11, 4.25), (11.5, 4.25)),
        ((13, 4.2), (13, 4.2))
    ]
    
    for start, end in main_arrows:
        arrow = FancyArrowPatch(start, end, arrowstyle='->', lw=2, color='black')
        ax.add_patch(arrow)
    
    # Training details
    train_box = FancyBboxPatch((1, 0.8), 12, 1, boxstyle="round,pad=0.1",
                               edgecolor='#F77F00', facecolor='#FCBF49', linewidth=2, linestyle='--')
    ax.add_patch(train_box)
    ax.text(7, 1.55, 'Fine-Tuning Configuration', ha='center', fontsize=11, fontweight='bold')
    ax.text(3.5, 1.15, 'Learning Rate: 2e-5', ha='center', fontsize=9)
    ax.text(7, 1.15, 'Batch Size: 32', ha='center', fontsize=9)
    ax.text(10.5, 1.15, 'Early Stopping: patience=3', ha='center', fontsize=9)
    
    # Accuracy
    ax.text(7, 0.2, f'Best Validation Accuracy: ~91.61% (BEST MODEL)', 
            ha='center', fontsize=12, bbox=dict(boxstyle='round', facecolor='#FFD700', alpha=0.7),
            fontweight='bold', color='#8B0000')
    
    plt.tight_layout()
    plt.savefig('api/models/diagrams/model4_distilbert.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Diagrama 4 generado: model4_distilbert.png")
    plt.close()

def create_comparison_summary():
    """Tabla comparativa final"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')
    
    # Título
    ax.text(0.5, 0.95, 'Comparación de Modelos - Sentiment Analysis', 
            ha='center', fontsize=18, fontweight='bold', transform=ax.transAxes)
    
    # Datos de la tabla
    models = ['Logistic Regression\n+ TF-IDF', 'Random Forest\n+ TF-IDF', 'LSTM\n(Optuna)', 'DistilBERT\n(Fine-tuned)']
    accuracy = ['88.40%', '85.12%', '87.38%', '91.61%']
    params = ['~20K features', '~200 trees', '~2.5M params', '~66M params']
    training = ['GridSearchCV\n3-fold', 'GridSearchCV\n3-fold', 'Optuna\n5-fold CV', 'Hugging Face\nTrainer']
    time = ['~2 min', '~5 min', '~15 min', '~45 min']
    
    # Colores por ranking
    colors = ['#FFE5B4', '#FFE5B4', '#FFD700', '#FFD700']
    
    # Crear tabla
    table_data = []
    for i in range(len(models)):
        table_data.append([models[i], accuracy[i], params[i], training[i], time[i]])
    
    table = ax.table(cellText=table_data,
                    colLabels=['Modelo', 'Accuracy', 'Parámetros', 'Optimización', 'Tiempo GPU'],
                    cellLoc='center',
                    loc='center',
                    bbox=[0.1, 0.15, 0.8, 0.7])
    
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)
    
    # Estilizar celdas
    for i in range(len(models) + 1):
        for j in range(5):
            cell = table[(i, j)]
            if i == 0:  # Header
                cell.set_facecolor('#4472C4')
                cell.set_text_props(weight='bold', color='white', fontsize=12)
            else:
                if j == 1:  # Columna de accuracy
                    cell.set_text_props(weight='bold', fontsize=12)
                cell.set_facecolor(colors[i-1])
                cell.set_edgecolor('black')
                cell.set_linewidth(1.5)
    
    # Leyenda
    ax.text(0.5, 0.08, '🏆 Mejor Modelo: DistilBERT (91.61%) - Transformer Architecture', 
            ha='center', fontsize=13, fontweight='bold', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#FFD700', alpha=0.8))
    
    ax.text(0.5, 0.02, 'Dataset: 50,000 IMDB reviews | GPU: NVIDIA A100 (Colab)', 
            ha='center', fontsize=10, style='italic', transform=ax.transAxes)
    
    plt.tight_layout()
    plt.savefig('api/models/diagrams/model_comparison_summary.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Tabla comparativa generada: model_comparison_summary.png")
    plt.close()

if __name__ == "__main__":
    import os
    os.makedirs('api/models/diagrams', exist_ok=True)
    
    print("\n" + "="*60)
    print("GENERANDO DIAGRAMAS DE ARQUITECTURA DE MODELOS")
    print("="*60 + "\n")
    
    create_logistic_regression_diagram()
    create_random_forest_diagram()
    create_lstm_diagram()
    create_distilbert_diagram()
    create_comparison_summary()
    
    print("\n" + "="*60)
    print("✅ TODOS LOS DIAGRAMAS GENERADOS EXITOSAMENTE")
    print("📁 Ubicación: api/models/diagrams/")
    print("="*60)
    print("\nArchivos generados:")
    print("  1. model1_logistic_regression.png")
    print("  2. model2_random_forest.png")
    print("  3. model3_lstm.png")
    print("  4. model4_distilbert.png")
    print("  5. model_comparison_summary.png")
    print("\n¡Listos para tu presentación! 🎯")
